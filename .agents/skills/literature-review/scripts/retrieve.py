#!/usr/bin/env python3
"""Small public-metadata adapter. Saves raw responses; never infers paper findings.

No credentials, shell execution, local secret discovery, or full-text downloads.
Each output directory is a new run; failed requests remain in the search log.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def clean(value):
    return re.sub(r'<[^>]+>', '', str(value or '')).strip()


def year_of(work):
    for field in ('published-print', 'published-online', 'published', 'issued'):
        parts = (work.get(field) or {}).get('date-parts') or []
        if parts and parts[0]:
            return parts[0][0]
    return None


def normalize(work, source, query_id):
    if source == 'crossref':
        authors = work.get('author') or []
        title = (work.get('title') or [''])[0]
        return dict(title=clean(title), authors=' and '.join(
            f"{a.get('family', '')}, {a.get('given', '')}".strip(', ') if a.get('family')
            else a.get('name', '') for a in authors), author=authors,
            first_author=authors[0].get('family', '') if authors else '',
            year=year_of(work), doi=str(work.get('DOI') or '').lower(),
            journal=(work.get('container-title') or [''])[0], volume=work.get('volume'),
            issue=work.get('issue'), pages=work.get('page'), article_number=work.get('article-number'),
            abstract=clean(work.get('abstract')), abstract_source='Crossref deposited abstract',
            url=work.get('URL'), type=work.get('type'), source=source, query_id=query_id,
            citations=work.get('is-referenced-by-count'), reading_status='metadata_only',
            correction_links=work.get('update-to', []))
    index = work.get('abstract_inverted_index') or {}
    words = {pos: word for word, positions in index.items() for pos in positions}
    authors = [a.get('author', {}).get('display_name', '') for a in work.get('authorships', [])]
    return dict(title=work.get('display_name', ''), authors=' and '.join(authors),
        year=work.get('publication_year'), doi=str(work.get('doi') or '').removeprefix('https://doi.org/').lower(),
        abstract=' '.join(words[i] for i in sorted(words)), abstract_source='OpenAlex inverted index',
        journal=((work.get('primary_location') or {}).get('source') or {}).get('display_name'),
        url=work.get('id'), source=source, query_id=query_id, citations=work.get('cited_by_count'),
        is_retracted=work.get('is_retracted'), open_access=work.get('open_access'),
        reading_status='metadata_only')


class Recorder:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=False)
        (self.directory / 'raw').mkdir()
        self.logs = []

    def get(self, url, query_id):
        # Fixed callers construct service URLs; no user-provided arbitrary URL fetch.
        host = urllib.parse.urlsplit(url).hostname
        if host not in ('api.crossref.org', 'api.openalex.org', 'api.semanticscholar.org'):
            raise ValueError('unsupported metadata service')
        log = dict(query_id=query_id, url=url, retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat())
        headers = {'User-Agent': 'ArchitectureLiteraturePilot/1.0', 'Accept': 'application/json'}
        if host == 'api.openalex.org' and os.environ.get('OPENALEX_API_KEY'):
            headers['Authorization'] = 'Bearer ' + os.environ['OPENALEX_API_KEY']
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=35) as response:
                data = response.read(20_000_001)
                if len(data) > 20_000_000:
                    raise ValueError('metadata response exceeds 20 MB')
                log['http_status'] = response.status
            result = json.loads(data)
            name = f'raw/{len(self.logs):03d}-{query_id}.json'
            (self.directory / name).write_bytes(data)
            log.update(raw_file=name, sha256=hashlib.sha256(data).hexdigest(), status='ok')
            return result
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            log.update(status='failed', error=str(exc))
            if isinstance(exc, urllib.error.HTTPError):
                log['http_status'] = exc.code
                log['retry_after'] = exc.headers.get('Retry-After')
            return None
        finally:
            self.logs.append(log)
            (self.directory / 'search-log.json').write_text(json.dumps(self.logs, ensure_ascii=False, indent=2)+'\n')


def search(args):
    plan = json.loads(Path(args.plan).read_text())
    run = Recorder(args.output)
    records = []
    blocked = set()
    for q in plan['queries']:
        if q['source'] not in ('crossref', 'openalex') or not 1 <= q['limit'] <= 100:
            raise ValueError('unsupported source or query limit')
        if q['source'] in blocked:
            run.logs.append(dict(query_id=q['id'], status='skipped_after_service_error'))
            continue
        params = {'search': q['query'], 'per_page': q['limit'], 'filter':
                  f'from_publication_date:{plan["from"]},to_publication_date:{plan["to"]}'} if q['source']=='openalex' else {
                  'query.bibliographic': q['query'], 'rows': q['limit'], 'filter':
                  f'from-pub-date:{plan["from"]},until-pub-date:{plan["to"]},type:journal-article'}
        host = 'api.openalex.org' if q['source']=='openalex' else 'api.crossref.org'
        payload = run.get(f'https://{host}/works?'+urllib.parse.urlencode(params), q['id'])
        if payload is not None:
            works = payload.get('results', []) if q['source']=='openalex' else payload['message']['items']
            log = run.logs[-1]
            log.update(exported_count=len(works), reported_total=payload.get('meta',{}).get('count') if q['source']=='openalex' else payload['message'].get('total-results'), exhaustive=False, cap=q['limit'])
            records.extend(normalize(w,q['source'],q['id']) for w in works)
        elif run.logs[-1].get('http_status') in (401,403,429):
            blocked.add(q['source'])
        time.sleep(1.1)
    (run.directory/'search-log.json').write_text(json.dumps(run.logs,ensure_ascii=False,indent=2)+'\n')
    (run.directory/'combined.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    (run.directory/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'records':len(records),'failed_queries':sum(x['status']=='failed' for x in run.logs)}))
    return int(any(x['status']!='ok' for x in run.logs))


def verify(args):
    records = json.loads(Path(args.input).read_text())
    run = Recorder(args.output)
    results = []
    openalex_available = True
    for i, record in enumerate(records, 1):
        doi = str(record['doi']).removeprefix('https://doi.org/').lower()
        if not re.fullmatch(r'10\.\d{4,9}/\S+',doi):
            raise ValueError('invalid DOI syntax')
        encoded = urllib.parse.quote(doi,safe='/')
        cr = run.get('https://api.crossref.org/works/'+encoded, f'crossref-{i:02d}')
        time.sleep(0.3)
        oa = run.get('https://api.openalex.org/works/https://doi.org/'+encoded, f'openalex-{i:02d}') if openalex_available else None
        if oa is None:
            openalex_available = False
        work = cr.get('message') if cr else None
        canonical = normalize(work,'crossref',f'verify-{i}') if work else record.copy()
        canonical['id'] = f'R{i:02d}'
        canonical['crossref_identity_verified'] = bool(work and str(work.get('DOI','')).lower()==doi)
        canonical['crossref_title_matches_search'] = clean(canonical['title']).casefold()==clean(record['title']).casefold()
        canonical['openalex_identity_verified'] = bool(oa and str(oa.get('doi','')).lower()=='https://doi.org/'+doi)
        canonical['openalex_title'] = oa.get('display_name') if oa else None
        canonical['openalex_year'] = oa.get('publication_year') if oa else None
        canonical['openalex_authors'] = [a.get('author',{}).get('display_name') for a in oa.get('authorships',[])] if oa else []
        canonical['is_retracted_openalex'] = oa.get('is_retracted') if oa else None
        if oa:
            n = normalize(oa,'openalex',f'verify-{i}')
            if not canonical.get('abstract'):
                canonical['abstract'],canonical['abstract_source']=n['abstract'],n['abstract_source']
            canonical['open_access']=oa.get('open_access')
            canonical['locations']=oa.get('locations',[])
        canonical['reading_status']='abstract_only' if canonical.get('abstract') else 'metadata_only'
        canonical['original_search_record']=record
        results.append(canonical)
        time.sleep(0.3)
    (run.directory/'verified-records.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    failed=[r['id'] for r in results if not r['crossref_identity_verified']]
    print(json.dumps({'records':len(results),'crossref_unresolved':failed,'openalex_verified':sum(r['openalex_identity_verified'] for r in results)}))
    return int(bool(failed))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('search');s.add_argument('--plan',required=True);s.add_argument('--output',required=True)
    v=sub.add_parser('verify');v.add_argument('--input',required=True);v.add_argument('--output',required=True)
    args=p.parse_args()
    return search(args) if args.command=='search' else verify(args)


if __name__=='__main__':
    raise SystemExit(main())

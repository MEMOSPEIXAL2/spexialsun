#!/usr/bin/env python3
"""Export reviewed records and human/agent annotations; never generate findings."""
import argparse
import csv
import json
import re
from pathlib import Path


def export(records, annotations, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)) or set(ids) != set(annotations):
        raise ValueError('record IDs and annotation IDs must match uniquely')
    rows, csl, ris, bib, refs = [], [], [], [], []
    for r in records:
        key = r['id']
        if not re.fullmatch(r'[A-Za-z0-9]+', key):
            raise ValueError('unsafe reference ID')
        a = annotations[key]
        if a['reading_status'] not in ('metadata_only', 'abstract_only', 'fulltext_sections_read', 'fulltext_read'):
            raise ValueError('unknown reading depth')
        if a['reading_status'] == 'metadata_only' and a.get('findings') not in ('', '未获取结论；不得按题名推断'):
            raise ValueError('metadata-only record cannot supply findings')
        row = {k:r.get(k,'') for k in ('id','title','authors','year','journal','doi')}
        row.update(a)
        rows.append(row)
        authors = r.get('author') or [{'literal':r.get('authors','')}]
        names = [{'family':x['family'], 'given':x.get('given','')} if x.get('family') else {'literal':x.get('literal') or x.get('name','')} for x in authors]
        citation = {'id':key,'type':'article-journal','title':r['title'],'author':names,
            'issued':{'date-parts':[[int(r['year'])]]},'container-title':r.get('journal',''),
            'DOI':r['doi'],'URL':'https://doi.org/'+r['doi']}
        for src,dest in [('volume','volume'),('issue','issue'),('pages','page'),('article_number','article-number')]:
            if r.get(src):citation[dest]=str(r[src])
        csl.append(citation)
        ris.extend(['TY  - JOUR',f'ID  - {key}',f'TI  - {r["title"]}'])
        for x in names:
            ris.append('AU  - '+ (f'{x["family"]}, {x.get("given","")}' if 'family' in x else x['literal']))
        ris.extend([f'PY  - {r["year"]}',f'JO  - {r.get("journal","")}',f'DO  - {r["doi"]}',f'UR  - https://doi.org/{r["doi"]}'])
        for src,dest in [('volume','VL'),('issue','IS')]:
            if r.get(src):ris.append(f'{dest}  - {r[src]}')
        if r.get('pages'):
            pages=re.split(r'[-–]',str(r['pages']),maxsplit=1)
            ris.append('SP  - '+pages[0])
            if len(pages)>1:ris.append('EP  - '+pages[1])
        elif r.get('article_number'):ris.append('SP  - '+str(r['article_number']))
        ris.extend([f'N1  - Reading status: {a["reading_status"]}; evidence: {a["locator"]}', 'ER  -', ''])
        fields={'title':r['title'],'author':r.get('authors',''),'year':str(r['year']),'journal':r.get('journal',''),'doi':r['doi']}
        for k in ('volume','issue','pages'):
            if r.get(k):fields['number' if k=='issue' else k]=str(r[k])
        if r.get('article_number') and not r.get('pages'):fields['eid']=str(r['article_number'])
        def escape(v):
            return str(v).replace('\\','\\textbackslash{}').replace('&','\\&').replace('%','\\%').replace('_','\\_').replace('#','\\#')
        bib.append('@article{'+key+',\n'+',\n'.join(f'  {k} = {{{escape(v)}}}' for k,v in fields.items())+'\n}\n')
        refs.append(f'[{key}] {r["authors"]} ({r["year"]}). {r["title"]}. {r.get("journal","")}. https://doi.org/{r["doi"]}')
    with (output/'evidence-matrix.csv').open('w',newline='',encoding='utf-8-sig') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    (output/'evidence-matrix.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    (output/'references.json').write_text(json.dumps(csl,ensure_ascii=False,indent=2)+'\n')
    (output/'references.ris').write_text('\n'.join(ris).rstrip()+'\n')
    (output/'references.bib').write_text('\n'.join(bib))
    (output/'references.md').write_text('# 核验后的文献题录\n\n以下为题录预览，正式 GB/T 7714 排版见 references-gbt7714.txt。\n\n'+'\n\n'.join(refs)+'\n')
    columns=['id','title','reading_status','method','findings','reviewer_appraisal','locator']
    table=['# 文献分析矩阵（摘要版）','','完整字段和作者见 evidence-matrix.csv。','','| '+' | '.join(columns)+' |','| '+' | '.join(['---']*len(columns))+' |']
    for row in rows:table.append('| '+' | '.join(str(row.get(k,'')).replace('|','/').replace('\n',' ') for k in columns)+' |')
    (output/'evidence-matrix.md').write_text('\n'.join(table)+'\n')
    return len(rows)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--records',required=True);p.add_argument('--annotations',required=True);p.add_argument('--output',required=True)
    a=p.parse_args()
    print('Exported',export(json.loads(Path(a.records).read_text()),json.loads(Path(a.annotations).read_text()),a.output),'records')


if __name__=='__main__':main()

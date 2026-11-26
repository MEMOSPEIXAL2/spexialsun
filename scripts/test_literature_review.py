"""Offline checks for provenance, failure handling and unsupported-claim rejection."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import urllib.error

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'.agents/skills/literature-review/scripts'


def load(name):
    spec=importlib.util.spec_from_file_location(name,SKILL/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


class ReviewTests(unittest.TestCase):
    def test_dedup_normalizes_doi_without_merging_distinct_dois(self):
        module=load('search_databases')
        records=[{'doi':'https://doi.org/10.1000/ABC','title':'A'},
                 {'doi':'10.1000/abc','title':'different metadata'},
                 {'doi':'10.1000/xyz','title':'A'},
                 {'title':'no DOI'}, {'title':'NO DOI'}]
        self.assertEqual(len(module.deduplicate_results(records)),3)

    def test_failed_network_request_is_preserved(self):
        module=load('retrieve')
        with tempfile.TemporaryDirectory() as tmp:
            recorder=module.Recorder(Path(tmp)/'run')
            error=urllib.error.HTTPError('https://api.openalex.org/works',429,'rate limited',{},None)
            with patch.object(module.urllib.request,'urlopen',side_effect=error):
                self.assertIsNone(recorder.get('https://api.openalex.org/works','OA01'))
            log=json.loads((Path(tmp)/'run/search-log.json').read_text())
            self.assertEqual(log[0]['status'],'failed')
            self.assertEqual(log[0]['http_status'],429)
            self.assertNotIn('Authorization',json.dumps(log))

    def test_credentials_only_reach_their_own_service(self):
        module=load('retrieve')
        with tempfile.TemporaryDirectory() as tmp, patch.dict(module.os.environ,{'OPENALEX_API_KEY':'test-not-a-real-key'}):
            recorder=module.Recorder(Path(tmp)/'run')
            with patch.object(module.urllib.request,'urlopen',side_effect=TimeoutError()) as call:
                recorder.get('https://api.crossref.org/works','CR01')
                self.assertNotIn('Authorization',dict(call.call_args.args[0].header_items()))
                recorder.get('https://api.openalex.org/works','OA01')
                self.assertEqual(dict(call.call_args.args[0].header_items()).get('Authorization'),'Bearer test-not-a-real-key')

    def test_metadata_only_cannot_supply_fabricated_findings(self):
        module=load('export_review')
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,'metadata-only'):
                module.export([{'id':'R01'}],{'R01':{'reading_status':'metadata_only','findings':'invented experiment'}},Path(tmp)/'out')

    def test_real_pilot_counts_identifiers_and_references(self):
        pilot=ROOT/'projects/renewable-materials-review'
        records=json.loads((pilot/'analysis/records.json').read_text())
        annotations=json.loads((pilot/'analysis/annotations.json').read_text())
        registration=json.loads((pilot/'verification/doi-registration.json').read_text())
        counts=json.loads((pilot/'analysis/flow-counts.json').read_text())
        self.assertEqual(len({r['doi'] for r in records}),15)
        self.assertEqual(set(annotations),{r['id'] for r in records})
        self.assertEqual(len(registration['verified']),15)
        self.assertFalse(registration['failed'])
        self.assertEqual(counts['records_available'],counts['pilot_sample']+counts['title_scope_exclusions']+counts['not_selected_pending_screening'])
        self.assertEqual(counts['pilot_sample'],counts['fulltext_read']+counts['abstract_only']+counts['metadata_only'])
        self.assertEqual((pilot/'outputs/references.ris').read_text().count('TY  - JOUR'),15)
        self.assertEqual(len(json.loads((pilot/'outputs/references.json').read_text())),15)


if __name__=='__main__':unittest.main()

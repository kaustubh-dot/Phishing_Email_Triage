"""Regression cases for portable setup and snapshot-specific human ratings."""
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

import pandas as pd

from submission_support import ensure_submission_assets, load_current_ratings, rating_snapshot_matches


def cases(reason='Current explanation'):
    return pd.DataFrame([{'email_id':f'{i:064x}', 'email':f'Email {i}',
        'dataset_label':'Safe Email', 'verdict':'safe', 'reason':reason,
        'quote':f'Email {i}', 'fallback_used':False, 'rater':'',
        'correctness_1_to_5':None, 'grounding_1_to_5':None,
        'usefulness_1_to_5':None, 'comment':''} for i in range(30)])


def rated(frame):
    result=frame.copy()
    result['rater']='Actual rater'
    result[['correctness_1_to_5','grounding_1_to_5','usefulness_1_to_5']]=4
    return result


class RatingTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'ratings.csv'

    def test_first_run_creates_blank_matching_sheet(self):
        result=load_current_ratings(cases(),self.path)
        self.assertTrue(self.path.exists())
        self.assertEqual(int(result['valid'].sum()),0)
        self.assertEqual(result['means'],{})
        self.assertTrue(rating_snapshot_matches(result['ratings'],cases()))

    def test_historical_ratings_never_count_for_new_reasons(self):
        rated(cases('Historical reason')).to_csv(self.path,index=False)
        before=self.path.read_bytes()
        current=load_current_ratings(cases(),self.path)
        self.assertNotEqual(current['path'],self.path)
        self.assertEqual(int(current['valid'].sum()),0)
        self.assertEqual(self.path.read_bytes(),before)
        self.assertEqual(load_current_ratings(cases(),self.path)['path'],current['path'])

    def test_matching_ratings_allow_reordering_and_compute_attribution(self):
        frame=rated(cases()).iloc[::-1]
        frame.to_csv(self.path,index=False)
        result=load_current_ratings(cases(),self.path)
        self.assertEqual(int(result['valid'].sum()),30)
        self.assertEqual(result['rater_counts'],{'Actual rater':30})
        self.assertTrue(all(value==4 for value in result['means'].values()))

    def test_changed_current_quote_is_rejected_without_overwrite(self):
        rated(cases('Old')).to_csv(self.path,index=False)
        current=load_current_ratings(cases(),self.path)['path']
        changed=rated(cases())
        changed.loc[0,'quote']='A quote from a different email'
        changed.to_csv(current,index=False)
        before=current.read_bytes()
        with self.assertRaisesRegex(ValueError,'does not match'):
            load_current_ratings(cases(),self.path)
        self.assertEqual(current.read_bytes(),before)

    def test_invalid_scores_and_missing_rater_do_not_count(self):
        frame=rated(cases())
        frame[['correctness_1_to_5','grounding_1_to_5','usefulness_1_to_5']] = frame[
            ['correctness_1_to_5','grounding_1_to_5','usefulness_1_to_5']].astype(object)
        frame.loc[0,'rater']='   '
        frame.loc[1,'correctness_1_to_5']=0
        frame.loc[2,'grounding_1_to_5']=6
        frame.loc[3,'usefulness_1_to_5']=2.5
        frame.loc[4,'correctness_1_to_5']='not a score'
        frame.to_csv(self.path,index=False)
        self.assertEqual(int(load_current_ratings(cases(),self.path)['valid'].sum()),25)

    def test_duplicate_cases_do_not_match(self):
        expected=cases()
        changed=rated(expected)
        changed.loc[1,'email_id']=changed.loc[0,'email_id']
        self.assertFalse(rating_snapshot_matches(changed,expected))

    def test_supplementary_assessment_fields_cannot_count_as_human_ratings(self):
        frame=cases().drop(columns=['rater','correctness_1_to_5',
                                   'grounding_1_to_5','usefulness_1_to_5'])
        frame['review_scope']='supplementary explanation assessment'
        frame['assessment_correctness_1_to_5']=5
        frame['assessment_grounding_1_to_5']=5
        frame['assessment_usefulness_1_to_5']=5
        frame.to_csv(self.path,index=False)
        result=load_current_ratings(cases(),self.path)
        self.assertEqual(int(result['valid'].sum()),0)
        self.assertEqual(result['rater_counts'],{})


class AssetTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def archive(self,files):
        buffer=BytesIO()
        with ZipFile(buffer,'w') as archive:
            for name,content in files.items(): archive.writestr('repo-abc/'+name,content)
        payload=buffer.getvalue()
        return lambda *args,**kwargs: BytesIO(payload)

    def test_missing_assets_are_verified_and_existing_human_work_is_preserved(self):
        files={'artifacts/model':b'weights','artifacts/ratings.csv':b'original ratings'}
        manifest={name:sha256(content).hexdigest() for name,content in files.items()}
        rating=self.root/'artifacts/ratings.csv'
        rating.parent.mkdir()
        rating.write_bytes(b'locally completed human work')
        result=ensure_submission_assets(self.root,manifest,'owner/repo','abc',opener=self.archive(files))
        self.assertEqual((self.root/'artifacts/model').read_bytes(),b'weights')
        self.assertEqual(rating.read_bytes(),b'locally completed human work')
        self.assertEqual(result['downloaded_files'],['artifacts/model'])
        def offline(*args,**kwargs): raise AssertionError('No network should be needed')
        self.assertEqual(ensure_submission_assets(self.root,manifest,'owner/repo','abc',opener=offline)['downloaded_files'],[])

    def test_checksum_failure_writes_no_partial_assets(self):
        files={'artifacts/good':b'good','artifacts/bad':b'corrupt'}
        manifest={'artifacts/good':sha256(b'good').hexdigest(),
                  'artifacts/bad':sha256(b'expected bytes').hexdigest()}
        with self.assertRaisesRegex(RuntimeError,'could not be downloaded and verified'):
            ensure_submission_assets(self.root,manifest,'owner/repo','abc',opener=self.archive(files))
        self.assertFalse((self.root/'artifacts/good').exists())

    def test_path_traversal_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'Unsafe asset path'):
            ensure_submission_assets(self.root,{'../outside':'invalid'},'owner/repo','abc')


if __name__=='__main__':
    unittest.main()

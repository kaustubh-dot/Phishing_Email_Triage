"""Bind confirmed human reviews to actual cases without creating numeric scores."""
import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd
from submission_support import human_review_snapshot, load_human_reviews

ROOT = Path(__file__).resolve().parents[1]


class HumanReviewSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.expected = pd.read_csv(ROOT/'artifacts/human_explanation_ratings_9b10d09848942b57.csv')
        self.records = self.expected.drop(columns=['rater', 'correctness_1_to_5',
            'grounding_1_to_5', 'usefulness_1_to_5', 'comment']).assign(
                reviewer='Project owner', review_status='complete', confirmation_source='Owner confirmation')
        self.confirmation = {'completed_human_reviews': 30,
            'reviewed_snapshot_sha256': human_review_snapshot(self.records),
            'evidence_type': 'owner-confirmed completion'}
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name)/'reviews.csv'
        self.records.to_csv(self.path, index=False)

    def test_exact_reviewed_cases_count_without_invented_numeric_scores(self):
        result = load_human_reviews(self.expected, self.path, self.confirmation)
        self.assertEqual(result['completed'], 30)
        self.assertTrue(result['snapshot_matches'])
        self.assertEqual(result['rater_counts'], {'Project owner': 30})
        self.assertNotIn('mean_human_ratings', result)

    def test_regenerated_explanations_do_not_inherit_completion(self):
        changed = self.expected.copy()
        changed.loc[0, 'reason'] = 'A different generated explanation.'
        result = load_human_reviews(changed, self.path, self.confirmation)
        self.assertFalse(result['snapshot_matches'])
        self.assertEqual(result['completed'], 0)
        self.assertEqual(result['confirmed_submission_reviews'], 30)

    def test_changed_review_record_is_rejected(self):
        self.records.loc[0, 'quote'] = 'Unrelated text'
        self.records.to_csv(self.path, index=False)
        with self.assertRaisesRegex(ValueError, 'confirmed snapshot'):
            load_human_reviews(self.expected, self.path, self.confirmation)

    def test_row_order_and_windows_newlines_are_accepted(self):
        self.records.iloc[::-1].to_csv(self.path, index=False, lineterminator='\r\n')
        self.assertEqual(load_human_reviews(self.expected, self.path, self.confirmation)['completed'], 30)


if __name__ == '__main__':
    unittest.main()

"""Portable prediction comparison and acceptance of completed human ratings."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('verifier',
    Path(__file__).resolve().parents[1]/'scripts/verify_submission_notebook.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class VerificationTests(unittest.TestCase):
    def test_completed_real_ratings_are_accepted(self):
        summary = {'human_ratings_required': 30, 'human_ratings_completed': 30,
                   'human_rating_snapshot_verified': True, 'human_rater_counts': {'Reviewer': 30}}
        verifier.validate_rating_summary(summary, {'human_ratings_completed': 30})

    def test_inconsistent_or_unverified_ratings_are_rejected(self):
        summary = {'human_ratings_required': 30, 'human_ratings_completed': 30,
                   'human_rating_snapshot_verified': True, 'human_rater_counts': {}}
        with self.assertRaises(ValueError):
            verifier.validate_rating_summary(summary, {'human_ratings_completed': 30})
        summary['human_rater_counts'] = {'Reviewer': 30}
        summary['human_rating_snapshot_verified'] = False
        with self.assertRaises(ValueError):
            verifier.validate_rating_summary(summary, {'human_ratings_completed': 30})

    def test_predictions_allow_windows_newlines_and_reordered_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            old, new = Path(directory)/'old.csv', Path(directory)/'new.csv'
            old.write_bytes(b'email_id,label,Model\na,0,0\nb,1,1\n')
            new.write_bytes(b'email_id,label,Model\r\nb,1,1\r\na,0,0\r\n')
            self.assertTrue(verifier.prediction_comparison(old, new)['matches'])
            new.write_bytes(b'email_id,label,Model\na,0,1\nb,1,1\n')
            report = verifier.prediction_comparison(old, new)
            self.assertFalse(report['matches'])
            self.assertEqual(report['different_rows_by_column']['Model'], 1)

    def test_missing_condition_is_not_reported_as_changed_predictions(self):
        with tempfile.TemporaryDirectory() as directory:
            old, new = Path(directory)/'old.csv', Path(directory)/'new.csv'
            old.write_text('email_id,label,Model,Other\na,0,0,1\n')
            new.write_text('email_id,label,Model\na,0,0\n')
            report = verifier.prediction_comparison(old, new)
            self.assertFalse(report['matches'])
            self.assertEqual(report['missing_columns'], ['Other'])
            self.assertEqual(report['different_rows_by_column'], {'label': 0, 'Model': 0})


if __name__ == '__main__':
    unittest.main()

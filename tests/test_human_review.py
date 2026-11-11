"""Protect human attribution and immutable explanation text during rating entry."""
import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('human_review',
    Path(__file__).resolve().parents[1]/'scripts/review_explanations.py')
human_review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(human_review)


class HumanReviewTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name)/'ratings.csv'
        self.rows = [{**{key: f'{key} {i}' for key in human_review.IMMUTABLE},
                      'rater': '', **{key: '' for key in human_review.DIMENSIONS}, 'comment': ''}
                     for i in range(2)]
        with self.path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(self.rows[0]))
            writer.writeheader()
            writer.writerows(self.rows)

    def test_rating_preserves_snapshot_and_other_rows(self):
        human_review.save_rating(self.path, 1, 'Reviewer', [3, 4, 2], 'Needs clearer reasoning')
        with self.path.open(encoding='utf-8', newline='') as stream:
            updated = list(csv.DictReader(stream))
        self.assertEqual(updated[1], self.rows[1])
        for key in human_review.IMMUTABLE:
            self.assertEqual(updated[0][key], self.rows[0][key])
        self.assertEqual(updated[0]['rater'], 'Reviewer')
        self.assertEqual(updated[0]['grounding_1_to_5'], '4')

    def test_invalid_scores_or_missing_name_leave_file_unchanged(self):
        original = self.path.read_bytes()
        for rater, scores in [('', [3, 4, 2]), ('Reviewer', [3, 6, 2]), ('Reviewer', [3, 2.5, 2])]:
            with self.assertRaises(ValueError):
                human_review.save_rating(self.path, 1, rater, scores)
            self.assertEqual(self.path.read_bytes(), original)

    def test_existing_rater_is_preserved_without_explicit_replacement(self):
        human_review.save_rating(self.path, 1, 'First reviewer', [3, 4, 2])
        original = self.path.read_bytes()
        with self.assertRaises(ValueError):
            human_review.save_rating(self.path, 1, 'Second reviewer', [5, 5, 5])
        self.assertEqual(self.path.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()

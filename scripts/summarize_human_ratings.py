"""Report completed human ratings for their original explanation snapshot."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from submission_support import load_human_reviews

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / 'artifacts/human_explanation_ratings.csv'
OUTPUT = ROOT / 'artifacts/results/full/human_rating_summary.json'
DIMENSIONS = ['correctness_1_to_5', 'grounding_1_to_5', 'usefulness_1_to_5']


def summarize():
    import pandas as pd

    with SHEET.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 30 or len({row['email_id'] for row in rows}) != 30:
        raise ValueError('The original human-rating sheet must contain 30 distinct cases.')
    scores = []
    for row in rows:
        values = [float(row[name]) for name in DIMENSIONS]
        if not row['rater'].strip() or not all(value.is_integer() and 1 <= value <= 5 for value in values):
            raise ValueError('Every completed rating needs a named rater and whole-number scores from 1 to 5.')
        scores.append(values)
    confirmation = json.loads((ROOT/'artifacts/human_review_confirmation.json').read_text(encoding='utf-8'))
    review_path = ROOT/confirmation['review_entries']
    current_cases = pd.read_csv(review_path)
    reviews = load_human_reviews(current_cases, review_path, confirmation)
    return {
        'rating_scope': 'original explanation snapshot',
        'human_rating_sheet': SHEET.relative_to(ROOT).as_posix(),
        'source_sha256': hashlib.sha256(SHEET.read_bytes()).hexdigest(),
        'human_ratings_completed': len(rows),
        'human_rater_counts': dict(Counter(row['rater'].strip() for row in rows)),
        'mean_human_ratings': {name: sum(row[i] for row in scores) / len(scores)
                               for i, name in enumerate(DIMENSIONS)},
        'current_human_based_reviews': {
            'status': 'complete', 'completed': reviews['completed'],
            'reviewer_counts': reviews['rater_counts'],
            'snapshot_verified': reviews['snapshot_matches'],
            'evidence_type': reviews['evidence_type'],
            'records': confirmation['review_entries'],
        },
        'scope_note': 'Numeric means describe the original saved explanations. The submitted snapshot has 30 owner-confirmed human-based reviews; numeric scores are not transferred between snapshots.',
    }


if __name__ == '__main__':
    summary = summarize()
    OUTPUT.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(summary, indent=2))

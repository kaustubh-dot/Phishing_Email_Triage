"""Collect a person's scores without changing exported explanation snapshots.

Example: python scripts/review_explanations.py --sheet artifacts/ratings_HASH.csv
         --rater "Your name" --start 1 --end 10
"""
import argparse
import csv
from io import StringIO
import os
from pathlib import Path
import tempfile

DIMENSIONS = ['correctness_1_to_5', 'grounding_1_to_5', 'usefulness_1_to_5']
IMMUTABLE = ['email_id', 'email', 'dataset_label', 'verdict', 'reason', 'quote', 'fallback_used']


def save_rating(path, case_number, rater, scores, comment='', *, replace=False):
    """Save one real entry atomically; preserve all case text and other raters."""
    path = Path(path)
    if not rater.strip():
        raise ValueError('Enter the actual rater name.')
    if len(scores) != 3 or not all(type(value) is int and 1 <= value <= 5 for value in scores):
        raise ValueError('Enter three whole-number scores between 1 and 5.')
    before = path.read_bytes()
    reader = csv.DictReader(StringIO(before.decode('utf-8'), newline=''))
    columns = reader.fieldnames
    rows = list(reader)
    if not set(IMMUTABLE + DIMENSIONS + ['rater', 'comment']).issubset(columns or []):
        raise ValueError('This is not an exported explanation-rating sheet.')
    if not 1 <= case_number <= len(rows):
        raise ValueError('Case number is outside the sheet.')
    row = rows[case_number-1]
    if not replace and (row['rater'].strip() or any(row[name].strip() for name in DIMENSIONS)):
        raise ValueError('This row already contains ratings; use --replace only to deliberately revise it.')
    row.update(rater=rater.strip(), comment=comment)
    row.update({name: str(value) for name, value in zip(DIMENSIONS, scores)})
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='',
                dir=path.parent, prefix=path.stem+'.', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            writer = csv.DictWriter(stream, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
        if path.read_bytes() != before:
            raise ValueError('The sheet changed while it was being reviewed. Reload it before saving.')
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sheet', type=Path, required=True)
    parser.add_argument('--rater', required=True)
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=30)
    parser.add_argument('--replace', action='store_true')
    args = parser.parse_args()
    if not args.rater.strip():
        parser.error('--rater must be the actual reviewer name.')
    with args.sheet.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    if not 1 <= args.start <= args.end <= len(rows):
        parser.error('--start and --end must select existing case numbers.')
    print('Read the email, displayed reason and quote. Score each dimension from 1 to 5.')
    print('Correctness: factual accuracy. Grounding: support in the quoted email.')
    print('Usefulness: how well the reason explains what to investigate. Ctrl+C stops safely.')
    for case in range(args.start, args.end+1):
        row = rows[case-1]
        if not args.replace and (row['rater'].strip() or any(row[name].strip() for name in DIMENSIONS)):
            print(f'Case {case}: existing rating preserved.')
            continue
        print(f'\nCASE {case} | email_id {row["email_id"]}')
        for name in ['email', 'verdict', 'reason', 'quote', 'fallback_used']:
            # Display untrusted source text as text; strip terminal control escapes.
            print(f'\n{name.upper()}:\n'+row[name].replace('\x1b', '[ESC]'))
        scores = []
        for dimension in DIMENSIONS:
            while True:
                value = input(f'{dimension} [1-5]: ').strip()
                if value in {'1', '2', '3', '4', '5'}:
                    scores.append(int(value))
                    break
                print('Enter one of 1, 2, 3, 4 or 5.')
        comment = input('Optional comment: ')
        save_rating(args.sheet, case, args.rater, scores, comment, replace=args.replace)
        print(f'Saved case {case}; the explanation snapshot is unchanged.')


if __name__ == '__main__':
    main()

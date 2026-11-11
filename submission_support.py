"""Single-notebook setup and explanation-rating validation.

Saved assets are read from a pinned public repository snapshot and checked before
being written. Human ratings count only when their immutable explanation fields
match the current run. No model inference or human scores are supplied here.
"""

from hashlib import sha256
from io import BytesIO
from pathlib import Path, PurePosixPath
from urllib.request import Request, urlopen
from zipfile import ZipFile


IMMUTABLE_RATING_COLUMNS = [
    'email_id', 'email', 'dataset_label', 'verdict', 'reason', 'quote', 'fallback_used',
]
RATING_COLUMNS = ['correctness_1_to_5', 'grounding_1_to_5', 'usefulness_1_to_5']


def human_review_snapshot(frame):
    """Identify exact reviewed cases, allowing CSV newlines and row reordering."""
    data = frame[IMMUTABLE_RATING_COLUMNS].copy().sort_values('email_id')
    for column in IMMUTABLE_RATING_COLUMNS:
        data[column] = data[column].fillna('').astype(str).str.replace('\r\n', '\n', regex=False)
    return sha256(data.to_json(orient='records', force_ascii=False).encode('utf-8')).hexdigest()


def load_human_reviews(expected, entries_path, confirmation):
    """Count owner-confirmed reviews only for their exact exported explanations.

    Review completion is separate from per-dimension numeric scores. This
    loader supplies no scores and never changes the submitted case text.
    """
    import pandas as pd

    if len(expected) != 30 or not expected.email_id.is_unique:
        raise ValueError('Human review requires 30 distinct explanation cases.')
    entries = pd.read_csv(entries_path)
    required = set(IMMUTABLE_RATING_COLUMNS + ['reviewer', 'review_status', 'confirmation_source'])
    if not required.issubset(entries.columns) or len(entries) != 30 or not entries.email_id.is_unique:
        raise ValueError('Invalid human-review completion records.')
    if human_review_snapshot(entries) != confirmation['reviewed_snapshot_sha256']:
        raise ValueError('Human-review records differ from their confirmed snapshot.')
    valid = entries.review_status.eq('complete') & entries.reviewer.fillna('').astype(str).str.strip().ne('')
    valid &= entries.confirmation_source.fillna('').astype(str).str.strip().ne('')
    confirmed_count = int(valid.sum())
    if confirmed_count != confirmation['completed_human_reviews']:
        raise ValueError('Human-review confirmation and completed records disagree.')
    matches = human_review_snapshot(expected) == confirmation['reviewed_snapshot_sha256']
    return {'completed': confirmed_count if matches else 0,
            'confirmed_submission_reviews': confirmed_count,
            'snapshot_matches': matches,
            'rater_counts': entries.loc[valid, 'reviewer'].value_counts().to_dict() if matches else {},
            'evidence_type': confirmation['evidence_type'], 'entries_path': str(entries_path)}


def ensure_submission_assets(root, manifest, repository, revision, *, opener=None):
    """Download missing, checksum-verified assets without replacing local files."""
    root = Path(root).resolve()
    targets = {}
    for name in manifest:
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError(f'Unsafe asset path: {name}')
        target = root.joinpath(*relative.parts)
        if not target.resolve().is_relative_to(root):
            raise ValueError(f'Asset path escapes the workspace: {name}')
        targets[name] = target
    missing = {name: target for name, target in targets.items() if not target.exists()}
    report = {'repository': repository, 'revision': revision,
              'existing_files_preserved': len(targets) - len(missing), 'downloaded_files': []}
    if not missing:
        return report
    url = f'https://codeload.github.com/{repository}/zip/{revision}'
    try:
        with (opener or urlopen)(Request(url, headers={'User-Agent': 'P13-notebook'}), timeout=120) as response:
            content = response.read(128 * 1024 * 1024 + 1)
        if len(content) > 128 * 1024 * 1024:
            raise ValueError('Repository download exceeds the 128 MiB setup limit.')
        prefix = f'{repository.split("/")[-1]}-{revision}/'
        verified = {}
        with ZipFile(BytesIO(content)) as archive:
            for name in missing:
                entry = archive.getinfo(prefix + name)
                if entry.file_size > 16 * 1024 * 1024:
                    raise ValueError(f'Unexpectedly large saved asset: {name}')
                payload = archive.read(entry)
                if sha256(payload).hexdigest() != manifest[name]:
                    raise ValueError(f'Saved asset checksum mismatch: {name}')
                verified[name] = payload
    except Exception as exc:
        raise RuntimeError(
            'Saved P13 assets are missing and could not be downloaded and verified. '
            'Enable internet for the first run, or copy the artifacts folder from '
            f'https://github.com/{repository}/tree/{revision} into {root}. '
            'Existing files have been preserved.'
        ) from exc
    # Validate the entire download before writing any file. Never overwrite local
    # adapters, rating sheets or other work, including a file created meanwhile.
    for name, payload in verified.items():
        target = missing[name]
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with target.open('xb') as stream:
                stream.write(payload)
        except FileExistsError:
            continue
        report['downloaded_files'].append(name)
    return report


def rating_snapshot_matches(frame, expected):
    """Require the exact cases, verdicts, reasons and quotes; allow row reordering."""
    required = set(IMMUTABLE_RATING_COLUMNS + RATING_COLUMNS + ['rater', 'comment'])
    if not required.issubset(frame.columns) or len(frame) != len(expected):
        return False
    if not frame.email_id.is_unique or not expected.email_id.is_unique:
        return False
    actual = frame.set_index('email_id').sort_index()
    wanted = expected.set_index('email_id').sort_index()

    def normalized_column(data, column):
        return data[column].fillna('').astype(str).str.replace('\r\n', '\n', regex=False)

    return actual.index.equals(wanted.index) and all(
        normalized_column(actual, column).equals(normalized_column(wanted, column))
        for column in IMMUTABLE_RATING_COLUMNS if column != 'email_id'
    )


def load_current_ratings(expected, base_path):
    """Create or load only the current snapshot and validate genuine rating fields."""
    import pandas as pd

    if len(expected) != 30 or not expected.email_id.is_unique:
        raise ValueError('Explanation evaluation requires 30 distinct fixed cases.')
    base_path = Path(base_path)
    base_path.parent.mkdir(parents=True, exist_ok=True)
    active_path = base_path
    preserved_path = None
    if base_path.exists() and not rating_snapshot_matches(pd.read_csv(base_path), expected):
        fingerprint = sha256(expected[IMMUTABLE_RATING_COLUMNS].to_json(
            orient='records', force_ascii=False).encode('utf-8')).hexdigest()[:16]
        active_path = base_path.with_name(f'{base_path.stem}_{fingerprint}.csv')
        preserved_path = base_path
    if not active_path.exists():
        expected.to_csv(active_path, index=False)
    ratings = pd.read_csv(active_path)
    if not rating_snapshot_matches(ratings, expected):
        raise ValueError(
            'The current rating sheet does not match the exact exported explanations. '
            'Preserve it and reconcile its immutable fields before counting any scores.'
        )
    numeric = ratings[RATING_COLUMNS].apply(pd.to_numeric, errors='coerce')
    valid = numeric.apply(lambda col: col.between(1, 5) & col.mod(1).eq(0)).all(axis=1)
    raters = ratings.rater.fillna('').astype(str).str.strip()
    valid &= raters.ne('')
    return {'path': active_path, 'preserved_path': preserved_path, 'ratings': ratings,
            'numeric': numeric, 'valid': valid,
            'rater_counts': raters.loc[valid].value_counts().to_dict(),
            'means': numeric.loc[valid].mean().to_dict() if valid.any() else {}}

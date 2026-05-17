import pandas as pd


REQUIRED_COLUMNS = {
    'in_theaters_date',
    'audience_rating',
    'tomatometer_rating',
    'genre',
}


def _validate_input_schema(df: pd.DataFrame) -> None:
    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))
    if missing:
        raise ValueError(
            'build_features is missing required columns: '
            + ', '.join(missing)
        )


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build model-friendly analytical features from a cleaned movie dataset.

    Expected input is already cleaned by src.cleaning.clean, but this function
    still applies defensive handling so it fails clearly on schema issues and
    behaves robustly with mixed types.
    """
    _validate_input_schema(df)
    out = df.copy()

    # Feature 1: year extracted from in-theaters date.
    in_theaters = pd.to_datetime(out['in_theaters_date'], errors='coerce')
    out['theater_year'] = in_theaters.dt.year

    # Feature 2: audience minus critics score (positive means audience is higher).
    out['audience_vs_critics'] = (
        pd.to_numeric(out['audience_rating'], errors='coerce')
        - pd.to_numeric(out['tomatometer_rating'], errors='coerce')
    )

    # Feature 3: primary genre from the first comma-separated token.
    out['primary_genre'] = (
        out['genre']
        .fillna('Unknown')
        .astype(str)
        .str.split(',')
        .str[0]
        .str.strip()
        .replace('', 'Unknown')
    )

    return out

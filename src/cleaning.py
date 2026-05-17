import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Fix MPAA rating typos (e.g. 'PG-13)' → 'PG-13')
    df = df.copy()
    df['rating'] = df['rating'].str.replace(')', '', regex=False).str.strip()

    # 2. Drop exact duplicates
    df = df.drop_duplicates()

    # 3. Parse date columns
    for col in ['in_theaters_date', 'on_streaming_date']:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # 4. Fill missing text fields
    df['critics_consensus'] = df['critics_consensus'].fillna('No consensus')
    df['genre'] = df['genre'].fillna('Unknown')
    df['studio_name'] = df['studio_name'].fillna('Unknown')
    df['directors'] = df['directors'].fillna('Unknown')
    df['writers'] = df['writers'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')

    # 5. Drop rows missing numeric essentials
    df = df.dropna(subset=['runtime_in_minutes', 'audience_rating', 'audience_count'])

    # 6. Convert tomatometer_status to ordered category
    status_order = ['Rotten', 'Fresh', 'Certified Fresh']
    df['tomatometer_status'] = pd.Categorical(
        df['tomatometer_status'], categories=status_order, ordered=True
    )

    return df.reset_index(drop=True)

from __future__ import annotations

import pandas as pd


EXPECTED_STATUS_ORDER = ['Rotten', 'Fresh', 'Certified Fresh']


def quality_checks(raw_df: pd.DataFrame, cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize the main cleaning impacts before and after processing."""
    raw_status = raw_df['tomatometer_status'] if 'tomatometer_status' in raw_df.columns else pd.Series(dtype='object')
    raw_valid_status = raw_status.dropna().isin(EXPECTED_STATUS_ORDER)

    metrics = [
        ('rows', len(raw_df), len(cleaned_df)),
        ('duplicate_rows', int(raw_df.duplicated().sum()), int(cleaned_df.duplicated().sum())),
        (
            'missing_runtime_in_minutes',
            int(raw_df['runtime_in_minutes'].isna().sum()) if 'runtime_in_minutes' in raw_df.columns else 0,
            int(cleaned_df['runtime_in_minutes'].isna().sum()) if 'runtime_in_minutes' in cleaned_df.columns else 0,
        ),
        (
            'missing_critics_consensus',
            int(raw_df['critics_consensus'].isna().sum()) if 'critics_consensus' in raw_df.columns else 0,
            int(cleaned_df['critics_consensus'].isna().sum()) if 'critics_consensus' in cleaned_df.columns else 0,
        ),
        (
            'unexpected_tomatometer_status',
            int((~raw_valid_status).sum()) if 'tomatometer_status' in raw_df.columns else 0,
            int(cleaned_df['tomatometer_status'].isna().sum()) if 'tomatometer_status' in cleaned_df.columns else 0,
        ),
    ]

    out = pd.DataFrame(metrics, columns=['metric', 'before', 'after'])
    out['delta'] = out['after'] - out['before']
    return out


def summarize_by_status(df: pd.DataFrame) -> pd.DataFrame:
    """Compare critic and audience scores by Tomatometer status."""
    summary = (
        df.groupby('tomatometer_status', observed=True, as_index=False)
        .agg(
            n_movies=('movie_title', 'count'),
            mean_audience_rating=('audience_rating', 'mean'),
            median_audience_rating=('audience_rating', 'median'),
            mean_tomatometer_rating=('tomatometer_rating', 'mean'),
            median_gap=('audience_vs_critics', 'median'),
        )
    )
    if 'tomatometer_status' in summary.columns:
        summary['tomatometer_status'] = pd.Categorical(
            summary['tomatometer_status'],
            categories=EXPECTED_STATUS_ORDER,
            ordered=True,
        )
        summary = summary.sort_values('tomatometer_status')
    return summary.reset_index(drop=True)


def summarize_genre_gap(df: pd.DataFrame, min_movies: int = 50) -> pd.DataFrame:
    """Summarize audience minus critics gap by primary genre."""
    summary = (
        df.groupby('primary_genre', as_index=False)
        .agg(
            n_movies=('movie_title', 'count'),
            mean_audience_rating=('audience_rating', 'mean'),
            mean_tomatometer_rating=('tomatometer_rating', 'mean'),
            median_gap=('audience_vs_critics', 'median'),
        )
    )
    summary = summary[summary['n_movies'] >= min_movies].copy()
    return summary.sort_values('median_gap', ascending=False).reset_index(drop=True)


def summarize_year_views(df: pd.DataFrame, min_movies: int = 5) -> pd.DataFrame:
    """Summarize typical audience_count by theater year."""
    summary = (
        df.groupby('theater_year', as_index=False)
        .agg(
            n_movies=('movie_title', 'count'),
            median_audience_count=('audience_count', 'median'),
            mean_audience_count=('audience_count', 'mean'),
        )
    )
    summary = summary[summary['n_movies'] >= min_movies].copy()
    return summary.sort_values('theater_year').reset_index(drop=True)


def summarize_rating_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize rating patterns by MPAA classification."""
    summary = (
        df.groupby('rating', as_index=False)
        .agg(
            n_movies=('movie_title', 'count'),
            mean_tomatometer_rating=('tomatometer_rating', 'mean'),
            median_tomatometer_rating=('tomatometer_rating', 'median'),
            mean_audience_rating=('audience_rating', 'mean'),
            median_audience_rating=('audience_rating', 'median'),
        )
    )
    return summary.sort_values('mean_tomatometer_rating', ascending=False).reset_index(drop=True)

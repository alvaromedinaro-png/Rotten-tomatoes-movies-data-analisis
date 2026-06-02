from src.config import RAW_PATH, OUT_PATH
from src.io import load_csv
from src.cleaning import clean
from src.features import build_features
from src.reporting import (
    quality_checks,
    summarize_by_status,
    summarize_genre_gap,
    summarize_rating_scores,
    summarize_year_views,
)
from src.utils import assert_columns
from src.viz import plot_graph


def main():
    raw_df = load_csv(RAW_PATH)
    cleaned_df = clean(raw_df)
    df = build_features(cleaned_df)
    assert_columns(df, ['tomatometer_rating', 'audience_rating', 'tomatometer_status',
                        'theater_year', 'audience_vs_critics', 'primary_genre'])

    print("\nQUALITY CHECKS")
    print(quality_checks(raw_df, cleaned_df).to_string(index=False))

    print("\nSTATUS SUMMARY")
    print(summarize_by_status(df).to_string(index=False))

    print("\nGENRE GAP SUMMARY")
    print(summarize_genre_gap(df).head(10).to_string(index=False))

    print("\nYEAR VIEWS SUMMARY")
    print(summarize_year_views(df).head(10).to_string(index=False))

    print("\nMPAA SUMMARY")
    print(summarize_rating_scores(df).to_string(index=False))

    plot_graph(df, out_dir=OUT_PATH.parent)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()

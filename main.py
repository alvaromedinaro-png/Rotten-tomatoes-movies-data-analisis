from src.config import RAW_PATH, OUT_PATH
from src.io import load_csv
from src.cleaning import clean
from src.features import build_features
from src.utils import assert_columns
from src.viz import plot_graph


def main():
    df = load_csv(RAW_PATH)
    df = clean(df)
    df = build_features(df)
    assert_columns(df, ['tomatometer_rating', 'audience_rating', 'tomatometer_status',
                        'theater_year', 'audience_vs_critics', 'primary_genre'])

    plot_graph(df, out_dir=OUT_PATH.parent)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()

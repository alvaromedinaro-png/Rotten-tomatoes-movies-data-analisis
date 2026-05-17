import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter, MaxNLocator
from pathlib import Path


def plot_graph(df: pd.DataFrame, out_dir: Path | None = None) -> None:
    def format_compact(x: float, _pos: float) -> str:
        if abs(x) >= 1_000_000:
            return f"{x / 1_000_000:.1f}M"
        if abs(x) >= 1_000:
            return f"{x / 1_000:.0f}K"
        return f"{x:.0f}"

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle("Rotten Tomatoes Movies – Exploratory Data Analysis", fontsize=16, fontweight="bold")

    # 1. Tomatometer Rating distribution
    sns.histplot(df['tomatometer_rating'], bins=20, kde=True, ax=axes[0, 0], color='tomato')
    axes[0, 0].set_title("Tomatometer Rating Distribution")
    axes[0, 0].set_xlabel("Tomatometer Rating (%)")
    axes[0, 0].set_ylabel("Count")

    # 2. Audience-vs-critics gap by genre (business-oriented comparison)
    gap_by_genre = (
        df.groupby('primary_genre', as_index=False)
        .agg(
            n_movies=('movie_title', 'count'),
            median_gap=('audience_vs_critics', 'median'),
        )
    )
    gap_by_genre = gap_by_genre[gap_by_genre['n_movies'] >= 50].copy()
    gap_by_genre = gap_by_genre.sort_values('median_gap', ascending=False).head(10)

    sns.barplot(
        data=gap_by_genre,
        x='median_gap',
        y='primary_genre',
        hue='primary_genre',
        palette='Set2',
        legend=False,
        ax=axes[0, 1],
    )
    axes[0, 1].axvline(0, color='black', linestyle='--', linewidth=1)
    axes[0, 1].set_title("Top géneros por gap público − crítica")
    axes[0, 1].set_xlabel("Mediana (Audience − Tomatometer)")
    axes[0, 1].set_ylabel("")

    # 3. Top genres by audience per movie (proportional, robust against volume bias)
    genre_views = (
        df.groupby('primary_genre', as_index=False)
        .agg(
            n_movies=('movie_title', 'count'),
            mean_audience_count=('audience_count', 'mean'),
        )
    )
    genre_views = genre_views[genre_views['n_movies'] >= 50].copy()
    top_genres_prop = genre_views.sort_values('mean_audience_count', ascending=False).head(10)

    sns.barplot(
        data=top_genres_prop,
        x='mean_audience_count',
        y='primary_genre',
        hue='primary_genre',
        ax=axes[0, 2],
        palette='viridis',
        legend=False,
    )
    axes[0, 2].set_title("Top 10 géneros por visualizaciones por película")
    axes[0, 2].set_xlabel("Audience count medio por película")
    axes[0, 2].set_ylabel("")
    axes[0, 2].xaxis.set_major_locator(MaxNLocator(nbins=6))
    axes[0, 2].xaxis.set_major_formatter(FuncFormatter(format_compact))
    for idx, row in top_genres_prop.reset_index(drop=True).iterrows():
        axes[0, 2].text(row['mean_audience_count'] + 0.01 * top_genres_prop['mean_audience_count'].max(), idx,
                        f"n={int(row['n_movies'])}", va='center', fontsize=8)

    # 4. Tomatometer vs Audience Rating scatter (coloured by status)
    status_order = ['Rotten', 'Fresh', 'Certified Fresh']
    palette = {'Rotten': '#e74c3c', 'Fresh': '#2ecc71', 'Certified Fresh': '#1a8a4a'}
    sns.scatterplot(
        data=df,
        x='tomatometer_rating',
        y='audience_rating',
        hue='tomatometer_status',
        hue_order=status_order,
        palette=palette,
        alpha=0.20,
        s=10,
        linewidth=0,
        ax=axes[1, 0],
    )
    # Diagonal reference: points above mean audience > critics, below means critics > audience.
    axes[1, 0].plot([0, 100], [0, 100], linestyle='--', color='black', linewidth=1)
    axes[1, 0].set_title("Tomatometer vs Audience Rating")
    axes[1, 0].set_xlabel("Tomatometer Rating (%)")
    axes[1, 0].set_ylabel("Audience Rating (%)")
    axes[1, 0].set_xlim(0, 100)
    axes[1, 0].set_ylim(0, 100)
    axes[1, 0].legend(markerscale=2, fontsize=8, title="Status")

    # 5. MPAA vs audience-vs-critics gap (median, with minimum sample threshold)
    mpaa_gap = (
        df.groupby('rating', as_index=False)
        .agg(
            n_movies=('movie_title', 'count'),
            median_gap=('audience_vs_critics', 'median'),
        )
    )
    mpaa_gap = mpaa_gap[mpaa_gap['n_movies'] >= 50].copy()
    mpaa_gap = mpaa_gap.sort_values('median_gap', ascending=False)

    sns.barplot(
        data=mpaa_gap,
        x='median_gap',
        y='rating',
        hue='rating',
        palette='Blues',
        legend=False,
        ax=axes[1, 1],
    )
    axes[1, 1].axvline(0, color='black', linestyle='--', linewidth=1)
    axes[1, 1].set_title("MPAA vs gap público − crítica")
    axes[1, 1].set_xlabel("Mediana (Audience − Tomatometer)")
    axes[1, 1].set_ylabel("MPAA Rating")

    for idx, row in mpaa_gap.reset_index(drop=True).iterrows():
        x_pos = row['median_gap'] + (0.2 if row['median_gap'] >= 0 else -0.6)
        axes[1, 1].text(x_pos, idx, f"n={int(row['n_movies'])}", va='center', fontsize=8)

    # 6. Top genres by audience rating (proportional, with minimum sample threshold)
    genre_pref = (
        df.groupby('primary_genre', as_index=False)
        .agg(
            n_movies=('movie_title', 'count'),
            mean_audience_rating=('audience_rating', 'mean'),
            median_audience_rating=('audience_rating', 'median'),
        )
    )
    genre_pref = genre_pref[genre_pref['n_movies'] >= 50].copy()
    top_preferred = genre_pref.sort_values('mean_audience_rating', ascending=False).head(10)

    sns.barplot(
        data=top_preferred,
        x='mean_audience_rating',
        y='primary_genre',
        hue='primary_genre',
        palette='crest',
        legend=False,
        ax=axes[1, 2],
    )
    axes[1, 2].set_title("Top géneros por preferencia del público")
    axes[1, 2].set_xlabel("Audience rating medio (%)")
    axes[1, 2].set_ylabel("")
    axes[1, 2].set_xlim(0, 100)

    for idx, row in top_preferred.reset_index(drop=True).iterrows():
        axes[1, 2].text(row['mean_audience_rating'] + 0.25, idx, f"n={int(row['n_movies'])}", va='center', fontsize=8)

    plt.tight_layout()

    if out_dir is not None:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        out_path = Path(out_dir) / "eda_visualizations.png"
        fig.savefig(out_path, dpi=150, bbox_inches='tight')
        print(f"Saved visualizations -> {out_path}")

    plt.show()

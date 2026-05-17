import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def plot_graph(df: pd.DataFrame, out_dir: Path | None = None) -> None:
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle("Rotten Tomatoes Movies – Exploratory Data Analysis", fontsize=16, fontweight="bold")

    # 1. Tomatometer Rating distribution
    sns.histplot(df['tomatometer_rating'], bins=20, kde=True, ax=axes[0, 0], color='tomato')
    axes[0, 0].set_title("Tomatometer Rating Distribution")
    axes[0, 0].set_xlabel("Tomatometer Rating (%)")
    axes[0, 0].set_ylabel("Count")

    # 2. Audience Rating by Tomatometer Status (boxplot)
    status_order = ['Rotten', 'Fresh', 'Certified Fresh']
    sns.boxplot(
        data=df,
        x='tomatometer_status',
        y='audience_rating',
        hue='tomatometer_status',
        order=status_order,
        palette='Set2',
        legend=False,
        ax=axes[0, 1],
    )
    axes[0, 1].set_title("Audience Rating by Tomatometer Status")
    axes[0, 1].set_xlabel("Tomatometer Status")
    axes[0, 1].set_ylabel("Audience Rating (%)")

    # 3. Top 10 Primary Genres (bar chart)
    top_genres = df['primary_genre'].value_counts().nlargest(10)
    sns.barplot(x=top_genres.values, y=top_genres.index, hue=top_genres.index,
               ax=axes[0, 2], palette='viridis', legend=False)
    axes[0, 2].set_title("Top 10 Primary Genres")
    axes[0, 2].set_xlabel("Number of Movies")
    axes[0, 2].set_ylabel("")
    total_genres = top_genres.sum()
    for idx, value in enumerate(top_genres.values):
        pct = 100 * value / total_genres
        axes[0, 2].text(value + 30, idx, f"{pct:.1f}%", va='center', fontsize=8)

    # 4. Tomatometer vs Audience Rating scatter (coloured by status)
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

    # 5. MPAA Rating distribution (bar chart)
    rating_counts = df['rating'].value_counts()
    axes[1, 1].bar(rating_counts.index, rating_counts.values, color='steelblue', edgecolor='white')
    axes[1, 1].set_title("MPAA Rating Distribution")
    axes[1, 1].set_xlabel("MPAA Rating")
    axes[1, 1].set_ylabel("Number of Movies")

    # 6. Audience-vs-Critics score gap distribution
    sns.histplot(df['audience_vs_critics'], bins=30, kde=True, ax=axes[1, 2], color='mediumpurple')
    axes[1, 2].axvline(0, color='black', linestyle='--', linewidth=1)
    axes[1, 2].axvline(df['audience_vs_critics'].median(), color='tomato', linestyle='-', linewidth=1.5)
    axes[1, 2].set_title("Audience Score − Critics Score Gap")
    axes[1, 2].set_xlabel("Audience Rating − Tomatometer (%)")
    axes[1, 2].set_ylabel("Count")

    plt.tight_layout()

    if out_dir is not None:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        out_path = Path(out_dir) / "eda_visualizations.png"
        fig.savefig(out_path, dpi=150, bbox_inches='tight')
        print(f"Saved visualizations -> {out_path}")

    plt.show()

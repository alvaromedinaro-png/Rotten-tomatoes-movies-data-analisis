import unittest
import sys
from pathlib import Path

import pandas as pd

# Allow running this file directly: python tests/test_cleaning_features.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.cleaning import clean
from src.features import build_features


class TestCleaningAndFeatures(unittest.TestCase):
    def test_clean_removes_rating_trailing_parenthesis_and_duplicates(self):
        raw = pd.DataFrame(
            {
                'movie_title': ['A', 'A', 'B'],
                'rating': ['PG-13)', 'PG-13)', 'R)'],
                'tomatometer_status': ['Fresh', 'Fresh', 'Rotten'],
                'in_theaters_date': ['2020-01-01', '2020-01-01', '2021-05-02'],
                'on_streaming_date': ['2020-06-01', '2020-06-01', '2021-10-01'],
                'critics_consensus': [None, None, 'ok'],
                'genre': ['Drama', 'Drama', 'Comedy'],
                'studio_name': ['S1', 'S1', 'S2'],
                'directors': ['D1', 'D1', 'D2'],
                'writers': ['W1', 'W1', 'W2'],
                'cast': ['C1', 'C1', 'C2'],
                'runtime_in_minutes': [100, 100, 90],
                'audience_rating': [80, 80, 70],
                'audience_count': [1000, 1000, 800],
                'tomatometer_rating': [75, 75, 65],
            }
        )

        out = clean(raw)

        self.assertEqual(len(out), 2)
        self.assertEqual(sorted(out['rating'].unique().tolist()), ['PG-13', 'R'])

    def test_clean_parses_dates_and_orders_status(self):
        raw = pd.DataFrame(
            {
                'movie_title': ['A', 'B', 'C'],
                'rating': ['PG', 'R', 'NR'],
                'tomatometer_status': ['Certified Fresh', 'Fresh', 'Rotten'],
                'in_theaters_date': ['2020-01-01', '2021-01-01', '2022-01-01'],
                'on_streaming_date': ['2020-06-01', '2021-06-01', '2022-06-01'],
                'critics_consensus': ['ok', 'ok', 'ok'],
                'genre': ['Drama', 'Comedy', 'Action'],
                'studio_name': ['S1', 'S2', 'S3'],
                'directors': ['D1', 'D2', 'D3'],
                'writers': ['W1', 'W2', 'W3'],
                'cast': ['C1', 'C2', 'C3'],
                'runtime_in_minutes': [100, 110, 95],
                'audience_rating': [80, 70, 60],
                'audience_count': [1000, 900, 800],
                'tomatometer_rating': [75, 65, 55],
            }
        )

        out = clean(raw)

        self.assertTrue(pd.api.types.is_datetime64_any_dtype(out['in_theaters_date']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(out['on_streaming_date']))
        self.assertIsInstance(out['tomatometer_status'].dtype, pd.CategoricalDtype)
        self.assertEqual(
            list(out['tomatometer_status'].cat.categories),
            ['Rotten', 'Fresh', 'Certified Fresh'],
        )

    def test_build_features_creates_expected_columns(self):
        base = pd.DataFrame(
            {
                'in_theaters_date': pd.to_datetime(['2020-03-04']),
                'audience_rating': [80],
                'tomatometer_rating': [70],
                'genre': ['Action & Adventure, Comedy'],
            }
        )

        out = build_features(base)

        self.assertIn('theater_year', out.columns)
        self.assertIn('audience_vs_critics', out.columns)
        self.assertIn('primary_genre', out.columns)
        self.assertEqual(out['theater_year'].astype('Int64').iloc[0], 2020)
        self.assertEqual(out['audience_vs_critics'].astype(float).iloc[0], 10.0)
        self.assertEqual(out.loc[0, 'primary_genre'], 'Action & Adventure')


if __name__ == '__main__':
    unittest.main()

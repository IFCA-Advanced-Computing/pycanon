import pandas as pd
import pytest

from pycanon import metrics
from pycanon.anonymity.utils import aux_functions


class TestMetrics:
    data_anon = aux_functions.read_file("./data/processed/adult_anonymized_3.csv")
    data_raw = aux_functions.read_file("./data/raw/adult.csv")
    data_raw.columns = data_raw.columns.str.strip()
    quasi_ident = [
        "age",
        "education",
        "occupation",
        "relationship",
        "sex",
        "native-country",
    ]
    sens_att = ["salary-class"]

    def test_aec(self):
        aec = metrics.average_ecsize(self.data_raw, self.data_anon, self.quasi_ident)
        assert isinstance(aec, float)

    def test_classification_metric(self):
        cm = metrics.classification_metric(
            self.data_raw, self.data_anon, self.quasi_ident, self.sens_att
        )
        assert isinstance(cm, float)

    def test_discernability_metric(self):
        dm = metrics.discernability_metric(
            self.data_raw, self.data_anon, self.quasi_ident
        )
        assert isinstance(dm, int) or isinstance(dm, float)

    def test_average_rir(self):
        avg_rir = metrics.average_rir(self.data_anon, self.quasi_ident)
        assert isinstance(avg_rir, float)

    def test_average_rir_value(self):
        avg_rir = metrics.average_rir(self.data_anon, self.quasi_ident)
        assert 0 <= avg_rir <= 1 / 3

    def test_max_rir(self):
        max_rir = metrics.max_rir(self.data_anon, self.quasi_ident)
        assert isinstance(max_rir, float)

    def test_max_rir_value(self):
        max_rir = metrics.max_rir(self.data_anon, self.quasi_ident)
        assert 0 <= max_rir <= 1 / 3

    def test_entropy_sa(self):
        entropy_sa = metrics.sa_entropy(self.data_anon, self.sens_att[0])
        assert isinstance(entropy_sa, float)

    def test_sizes_ec(self):
        stats_ec = metrics.sizes_ec(self.data_anon, self.quasi_ident)
        assert isinstance(stats_ec, dict)

    def test_sizes_ec_min(self):
        stats_ec = metrics.sizes_ec(self.data_anon, self.quasi_ident)
        assert stats_ec["min_ec"] == 3

    def test_sizes_ec_num(self):
        stats_ec = metrics.sizes_ec(self.data_anon, self.quasi_ident)
        assert stats_ec["n_ec"] <= len(self.data_anon) / 3

    def test_stats_quasi_ident_num(self):
        stats_qi = metrics.stats_quasi_ident(self.data_raw, "age")
        assert isinstance(stats_qi, dict)

    def test_stats_quasi_ident_cat(self):
        stats_qi = metrics.stats_quasi_ident(self.data_anon, "education")
        assert isinstance(stats_qi, dict)

    def test_stats_quasi_ident_error(self):
        with pytest.raises(ValueError):
            metrics.stats_quasi_ident(self.data_anon, "ages")

    def test_stats_quasi_ident_empty(self):
        empty_df = pd.DataFrame(columns=self.data_anon.columns)
        stats_qi = metrics.stats_quasi_ident(empty_df, "age")
        assert stats_qi == {}

    def test_stats_quasi_ident_freq(self):
        stats_qi = metrics.stats_quasi_ident(self.data_raw, "age")
        assert stats_qi["max_freq"] >= stats_qi["min_freq"]

    def test_stats_quasi_ident_mean(self):
        stats_qi = metrics.stats_quasi_ident(self.data_raw, "age")
        assert stats_qi["mean"] > 17 and stats_qi["mean"] < 90

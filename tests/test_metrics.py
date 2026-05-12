import numpy as np
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

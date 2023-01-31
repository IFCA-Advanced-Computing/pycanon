import numpy as np
import pytest

from pycanon import anonymity
from pycanon.anonymity.utils import aux_functions


class TestMathScores:
    qi = ['Teacher', 'Gender', 'Ethnic', 'Freeredu', 'wesson']
    sa = ['Score']
    file_name = './data/processed/StudentsMath_Score.csv'
    data = aux_functions.read_file(file_name)

    def test_k_anon(self):
        assert 1 == anonymity.k_anonymity(self.data, self.qi)

    def test_l_div(self):
        assert 1 == anonymity.l_diversity(self.data, self.qi, self.sa)

    def test_entropy_l(self):
        assert 1 == anonymity.entropy_l_diversity(self.data, self.qi, self.sa)

    def test_c_div(self):
        assert (np.nan, 1) == anonymity.recursive_c_l_diversity(
            self.data, self.qi, self.sa
        )

    def test_alpha(self):
        assert (1, 1) == anonymity.alpha_k_anonymity(self.data, self.qi, self.sa)

    def test_basic_beta(self):
        assert 71.0 == pytest.approx(
            anonymity.basic_beta_likeness(self.data, self.qi, self.sa)
        )

    def test_enhanced_beta(self):
        assert 5.375278407684164 == pytest.approx(
            anonymity.enhanced_beta_likeness(self.data, self.qi, self.sa)
        )

    def test_delta_disclosure(self):
        assert 4.276666119016055 == pytest.approx(
            anonymity.delta_disclosure(self.data, self.qi, self.sa)
        )

    def test_t_clos(self):
        assert 0.4165919952210274 == pytest.approx(
            anonymity.t_closeness(self.data, self.qi, self.sa)
        )

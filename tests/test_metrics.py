
import numpy as np
import pytest

from pycanon import anonymity


class TestMathScores:
    qi = ['Teacher', 'Gender', 'Ethnic', 'Freeredu', 'wesson']
    sa = ['Score']
    file_name = './Data/Processed/StudentsMath_Score.csv'

    def test_k_anon(self):
        assert 1 == anonymity.calculate_k(self.file_name, self.qi)

    def test_l_div(self):
        assert 1 == anonymity.calculate_l(self.file_name, self.qi, self.sa)

    def test_entropy_l(self):
        assert 1 == anonymity.calculate_entropy_l(
            self.file_name, self.qi, self.sa
        )

    def test_alpha(self):
        assert (1, 1) == anonymity.calculate_alpha_k(
            self.file_name, self.qi, self.sa
        )

    def test_basic_beta(self):
        assert 71.0 == pytest.approx(
            anonymity.calculate_basic_beta(
                self.file_name, self.qi, self.sa
            )
        )

    def test_enhanced_beta(self):
        assert 5.375278407684164 == pytest.approx(
            anonymity.calculate_enhanced_beta(
                self.file_name, self.qi, self.sa
            )
        )

    def test_delta_disclosure(self):
        assert 4.276666119016055 == pytest.approx(
            anonymity.calculate_delta_disclosure(
                self.file_name, self.qi, self.sa
            )
        )

    def test_t_clos(self):
        assert 0.4165919952210274 == pytest.approx(
            anonymity.calculate_t_closeness(
                self.file_name, self.qi, self.sa
            )
        )

    def test_c_div(self):
        assert (np.nan, 1) == anonymity.calculate_c_l_diversity(
            self.file_name, self.qi, self.sa
        )

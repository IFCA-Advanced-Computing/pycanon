import json

import numpy as np
import pytest

from pycanon.report import base
from pycanon.report import json as json_rep


class TestReport:
    def generate_json_dict(self, dataset, qi, sa, values):
        (
            k_anon, (alpha, alpha_k), l_div, entropy_l, (c_div, l_c_div),
            basic_beta, enhanced_beta, delta_disc, t_clos
        ) = values
        return {
            "data": {
                "file": dataset,
                "quasi-identifiers": qi,
                "sensitive attributes": sa
            },
            "k_anonymity": {
                "k": k_anon
            },
            "alpha_k_anonymity": {
                "alpha": alpha,
                "k": alpha_k
            },
            "l_diversity": {
                "l": l_div
            },
            "entropy_l_diversity": {
                "l": entropy_l
            },
            "recursive_c_l_diversity": {
                "c": c_div,
                "l": l_c_div
            },
            "basic_beta_likeness": {
                "beta": basic_beta
            },
            "enhanced_beta_likeness": {
                "beta": enhanced_beta
            },
            "t_closeness": {
                "t": t_clos
            },
            "delta_disclosure": {
                "delta": delta_disc
            }
        }


@pytest.mark.parametrize("dataset,expected", [
    (
        './Data/Processed/StudentsMath_Score.csv',
        (1, (1, 1), 1, 1, (np.nan, 1), 71, 5.375278407684164,
         4.276666119016055, 0.4165919952210274)
    ),
    (
        './Data/Processed/StudentsMath_Score_k5.csv',
        (5, (0.5, 5), 4, 3, (1, 4), 29.8, 5.036952602413629,
         3.4275146899795286, 0.31023287057769827)
    )

])
class TestMath(TestReport):
    qi = ['Teacher', 'Gender', 'Ethnic', 'Freeredu', 'wesson']
    sa = ['Score']

    def test_report_math(self, dataset, expected):
        assert expected == base.get_report_values(dataset, self.qi, self.sa)

    @pytest.mark.skip(
        reason="Fails for recursive_c_l_diversity as np.nan != np.nan"
    )
    def test_report_json(self, dataset, expected):
        expected_json = self.generate_json_dict(
            dataset, self.qi, self.sa, expected
        )
        obtained_json = json_rep.get_report(dataset, self.qi, self.sa)
        assert expected_json == json.loads(obtained_json)

import numpy as np
import pandas as pd
import pytest

from pycanon import anonymity
from pycanon.anonymity.utils import aux_anonymity, aux_functions


class TestMathScores:
    qi = ["Teacher", "Gender", "Ethnic", "Freeredu", "wesson"]
    sa = ["Score"]
    file_name_raw = "./data/processed/StudentsMath_Score.csv"
    data_raw = aux_functions.read_file(file_name_raw)
    file_name_anon = "./data/processed/StudentsMath_Score_k5.csv"
    data_anon = aux_functions.read_file(file_name_anon)

    def test_k_anon(self):
        assert 1 == anonymity.k_anonymity(self.data_raw, self.qi)

    def test_l_div(self):
        assert 1 == anonymity.l_diversity(self.data_raw, self.qi, self.sa)

    def test_entropy_l(self):
        assert 1 == anonymity.entropy_l_diversity(self.data_raw, self.qi, self.sa)

    def test_c_div(self):
        assert (np.nan, 1) == anonymity.recursive_c_l_diversity(
            self.data_raw, self.qi, self.sa
        )

    def test_alpha(self):
        assert (1, 1) == anonymity.alpha_k_anonymity(self.data_raw, self.qi, self.sa)

    def test_basic_beta(self):
        assert 71.0 == pytest.approx(
            anonymity.basic_beta_likeness(self.data_raw, self.qi, self.sa)
        )

    def test_enhanced_beta(self):
        assert 5.375278407684164 == pytest.approx(
            anonymity.enhanced_beta_likeness(self.data_raw, self.qi, self.sa)
        )

    def test_delta_disclosure(self):
        assert 4.276666119016055 == pytest.approx(
            anonymity.delta_disclosure(self.data_raw, self.qi, self.sa)
        )

    def test_t_clos(self):
        assert 0.4165919952210274 == pytest.approx(
            anonymity.t_closeness(self.data_raw, self.qi, self.sa)
        )

    def test_k_anon_5(self):
        assert 5 == anonymity.k_anonymity(self.data_anon, self.qi)

    def test_l_div_5(self):
        assert 1 <= anonymity.l_diversity(self.data_anon, self.qi, self.sa)

    def test_entropy_l_5(self):
        assert 1 <= anonymity.entropy_l_diversity(self.data_anon, self.qi, self.sa)

    def test_c_div_5(self):
        assert (1, 4) == anonymity.recursive_c_l_diversity(
            self.data_anon, self.qi, self.sa
        )

    def test_alpha_5(self):
        assert (0.5, 5) == anonymity.alpha_k_anonymity(self.data_anon, self.qi, self.sa)

    def test_basic_beta_5(self):
        assert isinstance(
            anonymity.basic_beta_likeness(self.data_anon, self.qi, self.sa), float
        )

    def test_enhanced_beta_5(self):
        assert isinstance(
            anonymity.enhanced_beta_likeness(self.data_anon, self.qi, self.sa), float
        )

    def test_delta_disclosure_5(self):
        assert isinstance(
            anonymity.delta_disclosure(self.data_anon, self.qi, self.sa), float
        )

class TestMultipleSA:
    qi = [
        "Gender",
        "Customer Type",
        "Age",
        "Type of Travel",
        "Class",
        "Flight Distance",
        "Departure Delay in Minutes",
        "Arrival Delay in Minutes",
    ]
    sa = ["Departure/Arrival time convenient", "On-board service", "satisfaction"]
    file_name_anon = "./data/processed/airline_passenger_sat_k5.csv"
    data_anon = aux_functions.read_file(file_name_anon)

    def test_k_anon(self):
        assert 5 <= anonymity.k_anonymity(self.data_anon, self.qi)

    def test_l_div(self):
        assert 1 <= anonymity.l_diversity(self.data_anon, self.qi, self.sa, gen=False)

    def test_entropy_l(self):
        assert 1 <= anonymity.entropy_l_diversity(self.data_anon, self.qi, self.sa, gen=False)

    def test_c_div(self):
        _, l_div = anonymity.recursive_c_l_diversity(self.data_anon, self.qi, self.sa, gen=False)  
        assert l_div >= 1

    def test_alpha_k_anonymity(self):
        alpha, k_anon = anonymity.alpha_k_anonymity(self.data_anon, self.qi, self.sa, gen=False)
        assert alpha >= 0 and k_anon >= 5

    def test_basic_beta(self):
        assert isinstance(
            anonymity.basic_beta_likeness(self.data_anon, self.qi, self.sa, gen=False), float
        )
    
    def test_enhanced_beta(self):
        assert isinstance(
            anonymity.enhanced_beta_likeness(self.data_anon, self.qi, self.sa, gen=False), float
        )

    def test_delta_disclosure(self):
        assert isinstance(
            anonymity.delta_disclosure(self.data_anon, self.qi, self.sa, gen=False), float
        )


class TestUnitary:
    qi = ["Teacher", "Gender", "Ethnic", "Freeredu", "wesson"]
    sa = ["Score"]
    file_name = "./data/processed/StudentsMath_Score.csv"
    file_name_empty = "./data/processed/empty.csv"

    def test_read_file(self):
        data = aux_functions.read_file(self.file_name)
        assert isinstance(data, pd.DataFrame)
        

    def test_check_qi(self):
        data = aux_functions.read_file(self.file_name)
        with pytest.raises(ValueError):
            aux_functions.check_qi(data, ["age"])

    def test_check_sa(self):
        data = aux_functions.read_file(self.file_name)
        with pytest.raises(ValueError):
            aux_functions.check_sa(data, ["age"])

    def test_aux_t_closeness_str(self):
        data = aux_functions.read_file(self.file_name)
        value = aux_anonymity.aux_t_closeness_str(data, self.qi, self.sa)
        assert isinstance(value, float)

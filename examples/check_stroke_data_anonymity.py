# -*- coding: utf-8 -*-

# Copyright 2022 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Example using the stroke prediction dataset."""

import numpy as np
import pandas as pd
from pycanon import anonymity


def anonymity_level(file_name, quasi_ident, sens_att):
    """Function for check all the anonymity techniques under study."""
    data = pd.read_csv(file_name)
    k_anon = anonymity.k_anonymity(data, quasi_ident)
    l_div = anonymity.l_diversity(data, quasi_ident, sens_att)
    entropy_l = anonymity.entropy_l_diversity(data, quasi_ident, sens_att)
    alpha, _ = anonymity.alpha_k_anonymity(data, quasi_ident, sens_att)
    basic_beta = anonymity.basic_beta_likeness(data, quasi_ident, sens_att)
    enhanced_beta = anonymity.enhanced_beta_likeness(data, quasi_ident, sens_att)
    delta_disclosure = anonymity.delta_disclosure(data, quasi_ident, sens_att)
    t_clos = anonymity.t_closeness(data, quasi_ident, sens_att)
    c_div, _ = anonymity.recursive_c_l_diversity(data, quasi_ident, sens_att)

    print(
        f"""File: {file_name}. The dataset verifies:
    \t - k-anonymity with k = {k_anon}
    \t - (alpha,k)-anonymity with alpha = {alpha} and k = {k_anon}
    \t - l-diversity with l = {l_div}
    \t - entropy l-diversity with l = {entropy_l}
    \t - basic beta-likeness with beta = {basic_beta}
    \t - enhanced beta-likeness with beta = {enhanced_beta}
    \t - delta-disclosure privacy with delta = {delta_disclosure}
    \t - t-closeness with t = {t_clos}"""
    )
    if np.isnan(c_div):
        print(
            f"\t - As l = {l_div} for l-diversity, "
            f"c cannot be calculated for (c,l)-diversity.\n"
        )
    else:
        print(f"\t - (c,l)-diversity with c = {c_div} and l = {l_div}.\n")


QI = [
    "gender",
    "age",
    "hypertension",
    "heart_disease",
    "ever_married",
    "work_type",
    "Residence_type",
    "smoking_status",
]
SA = ["stroke"]
FILE_NAME = "../data/processed/healthcare-dataset-stroke-data.csv"
anonymity_level(FILE_NAME, QI, SA)

for i in [2, 5, 10, 15, 19, 20, 22, 25]:
    FILE_NAME = f"../data/processed/stroke_k{i}.csv"
    anonymity_level(FILE_NAME, QI, SA)

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

"""Get report values for all privacy models."""

from typing import Tuple, Any

import pandas as pd

from pycanon import anonymity


def get_report_values(
    data: pd.DataFrame, quasi_ident: list, sens_att: list, gen=True
) -> Tuple[
    int, Tuple[float, int], int, float, Tuple[Any, int], float, float, float, float
]:
    """Generate a report with the parameters obtained for each anonymity check.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: is a list of strings

    :param gen: default to true. If true it is generalized for the case of
        multiple SA, if False, the set of QI is updated for each SA.
    :type gen: boolean
    """
    k_anon = anonymity.k_anonymity(data, quasi_ident)
    alpha, alpha_k = anonymity.alpha_k_anonymity(data, quasi_ident, sens_att, gen)
    l_div = anonymity.l_diversity(data, quasi_ident, sens_att, gen)
    entropy_l = anonymity.entropy_l_diversity(data, quasi_ident, sens_att, gen)
    c_div, l_c_div = anonymity.recursive_c_l_diversity(data, quasi_ident, sens_att, gen)
    basic_beta = anonymity.basic_beta_likeness(data, quasi_ident, sens_att, gen)
    enhanced_beta = anonymity.enhanced_beta_likeness(data, quasi_ident, sens_att, gen)
    delta_disc = anonymity.delta_disclosure(data, quasi_ident, sens_att, gen)
    t_clos = anonymity.t_closeness(data, quasi_ident, sens_att, gen)

    return (
        k_anon,
        (alpha, alpha_k),
        l_div,
        entropy_l,
        (c_div, l_c_div),
        basic_beta,
        enhanced_beta,
        delta_disc,
        t_clos,
    )

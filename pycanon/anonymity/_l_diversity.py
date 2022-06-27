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

import typing

import numpy as np
import pandas as pd

from pycanon.anonymity.utils import aux_anonymity
from pycanon.anonymity.utils import aux_functions


def l_diversity(data: pd.DataFrame,
                quasi_ident: typing.List,
                sens_att: typing.List,
                gen=True) -> int:
    """Calculate l for l-diversity.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: list of strings

    :param gen: boolean, default to True. If true, it is generalized for the
        case of multiple SA, if False, the set of QI is updated for each SA
    :type  gen: boolean

    :return: l value for l-diversity.
    :rtype: int.
    """
    quasi_ident = np.array(quasi_ident)
    sens_att = np.array(sens_att)
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)

    equiv_class = aux_anonymity.get_equiv_class(data, quasi_ident)
    l_div = []
    if gen:
        for ec in equiv_class:
            data_temp = data.iloc[aux_functions.convert(ec)]
            l_sa = [len(np.unique(data_temp[sa].values)) for sa in sens_att]
            l_div.append(min(l_sa))
    else:
        for i, sa in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            equiv_class = aux_anonymity.get_equiv_class(data, tmp_qi)
            l_ec = []
            for ec in equiv_class:
                data_temp = data.iloc[aux_functions.convert(ec)]
                l_ec.append(len(np.unique(data_temp[sa].values)))
            l_div.append(min(l_ec))
    return min(l_div)

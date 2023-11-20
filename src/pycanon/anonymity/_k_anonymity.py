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


def k_anonymity(
    data: pd.DataFrame, quasi_ident: typing.Union[typing.List, np.ndarray]
) -> int:
    """Calculate k for k-anonymity.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :return: k value for k-anonymity.
    :rtype: int.
    """
    aux_functions.check_qi(data, quasi_ident)

    equiv_class = aux_anonymity.get_equiv_class(data, quasi_ident)
    k_anon = min([len(x) for x in equiv_class])
    return k_anon


def alpha_k_anonymity(
    data: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: typing.Union[typing.List, np.ndarray],
    gen=True,
) -> typing.Tuple[float, int]:
    """Calculate alpha and k for (alpha,k)-anonymity.

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

    :return: alpha and k values for (alpha,k)-anonymity.
    :rtype: alpha is a float, k is an int.
    """
    quasi_ident = np.array(quasi_ident)
    sens_att = np.array(sens_att)
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)
    k_anon = k_anonymity(data, quasi_ident)
    equiv_class = aux_anonymity.get_equiv_class(data, quasi_ident)
    if gen:
        alpha_ec = []
        for ec in equiv_class:
            data_temp = data.iloc[aux_functions.convert(ec)]
            alpha_sa = []
            for sa in sens_att:
                values = np.unique(data_temp[sa].values)
                _alpha = [
                    len(data_temp[data_temp[sa] == s]) / len(data_temp) for s in values
                ]
                alpha_sa.append(max(_alpha))
            alpha_ec.append(max(alpha_sa))
        alpha = max(alpha_ec)
    else:
        alpha_sa = []
        for i, sa in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            equiv_class = aux_anonymity.get_equiv_class(data, tmp_qi)
            alpha_ec = []
            for ec in equiv_class:
                data_temp = data.iloc[aux_functions.convert(ec)]
                values = np.unique(data_temp[sa].values)
                _alpha = [
                    len(data_temp[data_temp[sa] == s]) / len(data_temp) for s in values
                ]
                alpha_ec.append(max(_alpha))
            alpha_sa.append(max(alpha_ec))
        alpha = max(alpha_sa)
    return alpha, k_anon

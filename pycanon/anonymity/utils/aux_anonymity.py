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

"""
Module with different functions which calculate properties about anonymity.

k-anonymity, (alpha,k)-anonymity, l-diversity, entropy l-diversity,
(c,l)-diversity, basic beta-likeness, enhanced beta-likeness, t-closeness and
delta-disclosure privacy.
"""

import numpy as np
import pandas as pd
from pycanon.anonymity.utils import aux_functions

from typing import Tuple, Union


def get_equiv_class(data: pd.DataFrame, quasi_ident: Union[list, np.ndarray]) -> list:
    """Find the equivalence classes present in the dataset.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are the quasi-identifiers.
    :type quasi_ident: is a list of strings

    :return: equivalence classes.
    :rtype: list.
    """
    if isinstance(quasi_ident, np.ndarray):
        quasi_ident = quasi_ident.tolist()
    df_grouped = data.groupby(by=quasi_ident)
    equiv_class = []
    for ec in df_grouped.groups.values():
        equiv_class.append(np.array(ec.tolist()))
    return equiv_class


def aux_calculate_beta(
    data: pd.DataFrame, quasi_ident: Union[list, np.ndarray], sens_att_value: str
) -> Tuple[np.ndarray, list]:
    """Beta calculation for basic and enhanced beta-likeness.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att_value: sensitive attribute under study.
    :type sens_att_value: string

    :return: proportion of each value of the sensitive attribute in the entire
        database and distance from the proportion in each equivalence class.
    :rtype: np.array and list.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    p = np.array([len(data[data[sens_att_value] == s]) / len(data) for s in values])
    q = []
    for ec in equiv_class:
        data_temp = data.iloc[aux_functions.convert(ec)]
        qi = np.array(
            [len(data_temp[data_temp[sens_att_value] == s]) / len(ec) for s in values]
        )
        q.append(qi)
    dist = [max((q[i] - p) / p) for i in range(len(equiv_class))]
    return p, dist


def aux_calculate_delta_disclosure(
    data: pd.DataFrame, quasi_ident: Union[list, np.ndarray], sens_att_value: str
) -> float:
    """Delta calculation for delta-disclosure privacy.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att_value: sensitive attribute under study.
    :type sens_att_value: string

    :return: delta for the introduced SA.
    :rtype: float.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    p = np.array([len(data[data[sens_att_value] == s]) / len(data) for s in values])
    q = []
    for ec in equiv_class:
        data_temp = data.iloc[aux_functions.convert(ec)]
        qi = np.array(
            [len(data_temp[data_temp[sens_att_value] == s]) / len(ec) for s in values]
        )
        q.append(qi)
    aux = [max([np.abs(np.log(x)) for x in qi / p if x > 0]) for qi in q]
    return max(aux)


def aux_t_closeness_num(
    data: pd.DataFrame, quasi_ident: Union[list, np.ndarray], sens_att_value: str
) -> float:
    """Obtain t for t-closeness.

    Function used for numerical attributes: the definition of the EMD is used.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att_value: sensitive attribute under study.
    :type sens_att_value: string

    :return: t for the introduced SA (numerical).
    :rtype: float.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    m = len(values)
    p = np.array([len(data[data[sens_att_value] == s]) / len(data) for s in values])
    emd = []
    for ec in equiv_class:
        data_temp = data.iloc[aux_functions.convert(ec)]
        qi = np.array(
            [len(data_temp[data_temp[sens_att_value] == s]) / len(ec) for s in values]
        )
        r = qi - p
        abs_r, emd_ec = 0.0, 0.0
        for i in range(m):
            abs_r += r[i]
            emd_ec += np.abs(abs_r)
        emd_ec = 1 / (m - 1) * emd_ec
        emd.append(emd_ec)
    return max(emd)


def aux_t_closeness_str(
    data: pd.DataFrame, quasi_ident: Union[list, np.ndarray], sens_att_value: list
) -> float:
    """Obtain t for t-closeness.

    Function used for categorical attributes: the metric "Equal Distance" is
    used.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att_value: sensitive attribute under study.
    :type sens_att_value: string

    :return: t for the introduced SA (categorical).
    :rtype: float.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    m = len(values)
    p = np.array([len(data[data[sens_att_value] == s]) / len(data) for s in values])
    emd = []
    for ec in equiv_class:
        data_temp = data.iloc[aux_functions.convert(ec)]
        qi = np.array(
            [len(data_temp[data_temp[sens_att_value] == s]) / len(ec) for s in values]
        )
        r = qi - p
        emd_ec = 0.0
        for i in range(m):
            emd_ec += np.abs(r[i])
        emd_ec = 0.5 * emd_ec
        emd.append(emd_ec)
    return max(emd)

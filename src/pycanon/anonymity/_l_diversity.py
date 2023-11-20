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


def l_diversity(
    data: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: typing.Union[typing.List, np.ndarray],
    gen=True,
) -> int:
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


def entropy_l_diversity(
    data: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: typing.Union[typing.List, np.ndarray],
    gen=True,
) -> float:
    """Calculate l for entropy l-diversity.

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

    :return: l value for entropy l-diversity.
    :rtype: float.
    """
    quasi_ident = np.array(quasi_ident)
    sens_att = np.array(sens_att)
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)

    if gen:
        equiv_class = aux_anonymity.get_equiv_class(data, quasi_ident)
        entropy_ec = []
        for ec in equiv_class:
            data_temp = data.iloc[aux_functions.convert(ec)]
            entropy_sa = []
            for sa in sens_att:
                values = np.unique(data_temp[sa].values)
                p = [
                    len(data_temp[data_temp[sa] == s]) / len(data_temp) for s in values
                ]
                entropy = np.sum(p * np.log(p))
                entropy_sa.append(-entropy)
            entropy_ec.append(min(entropy_sa))
        ent_l = int(min(np.exp(1) ** entropy_ec))
    else:
        entropy_sa = []
        for i, sa in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            equiv_class = aux_anonymity.get_equiv_class(data, tmp_qi)
            entropy_ec = []
            for ec in equiv_class:
                data_temp = data.iloc[aux_functions.convert(ec)]
                entropy = 0
                values = np.unique(data_temp[sa].values)
                p = [
                    len(data_temp[data_temp[sa] == s]) / len(data_temp) for s in values
                ]
                entropy = np.sum(p * np.log(p))
                entropy_ec.append(-entropy)
            entropy_sa.append(min(entropy_ec))
        ent_l = int(min(np.exp(1) ** entropy_sa))
    return ent_l


def recursive_c_l_diversity(
    data: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: typing.Union[typing.List, np.ndarray],
    imp=False,
    gen=True,
) -> typing.Tuple[float, int]:
    """Calculate c and l for recursive (c,l)-diversity.

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

    :return: c and l values for recursive (c,l)-diversity.
    :rtype: c is a float, l is an int.
    """
    quasi_ident = np.array(quasi_ident)
    sens_att = np.array(sens_att)
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)
    l_div = l_diversity(data, quasi_ident, sens_att)
    if l_div > 1:
        c_div_aux = []
        if gen:
            equiv_class = aux_anonymity.get_equiv_class(data, quasi_ident)
            for sens_att_value in sens_att:
                c_sa = []
                for ec in equiv_class:
                    data_temp = data.iloc[aux_functions.convert(ec)]
                    values = np.unique(data_temp[sens_att_value].values)
                    r_ec = np.sort(
                        [len(data_temp[data_temp[sens_att_value] == s]) for s in values]
                    )
                    c_sa.append(
                        np.floor(r_ec[0] / sum(r_ec[l_div - 1 :]) + 1)  # noqa: E203
                    )
                c_div_aux.append(int(max(c_sa)))
        else:
            for i, sa in enumerate(sens_att):
                tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
                equiv_class = aux_anonymity.get_equiv_class(data, tmp_qi)
                c_sa = []
                for ec in equiv_class:
                    data_temp = data.iloc[aux_functions.convert(ec)]
                    values = np.unique(data_temp[sa].values)
                    r_ec = np.sort([len(data_temp[data_temp[sa] == s]) for s in values])
                    c_sa.append(
                        np.floor(r_ec[0] / sum(r_ec[l_div - 1 :]) + 1)  # noqa: E203
                    )
                c_div_aux.append(int(max(c_sa)))
        c_div = np.max(c_div_aux)
    else:
        if imp:
            print(f"c for (c,l)-diversity cannot be calculated as l={l_div}")
        c_div = np.nan
    return c_div, l_div


def _achieve_l_diversity(
    data: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: typing.Union[typing.List, np.ndarray],
    l_new: int,
) -> pd.DataFrame:
    """Transform dataset checking l-diversity for l, using suppression.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: list of strings

    :param l_new: l value for l-diversity.
    :type l_new: int

    :return: dataframe verifying l-diversity for l_new.
    :rtype: pandas dataframe.
    """
    quasi_ident = np.array(quasi_ident)
    sens_att = np.array(sens_att)
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)
    equiv_class = aux_anonymity.get_equiv_class(data, quasi_ident)
    l_ec = []
    for ec in equiv_class:
        data_temp = data.iloc[aux_functions.convert(ec)]
        l_sa = [len(np.unique(data_temp[sa].values)) for sa in sens_att]
        l_ec.append(min(l_sa))
    aux = pd.DataFrame({"equiv_class": equiv_class, "l_ec": l_ec})
    data_ec_l = aux[aux.l_ec < l_new]
    ec_elim = np.concatenate(
        [aux_functions.convert(x) for x in data_ec_l.equiv_class.values]
    )
    data_new = data.drop(ec_elim).reset_index()
    data_new.drop("index", inplace=True, axis=1)
    return data_new

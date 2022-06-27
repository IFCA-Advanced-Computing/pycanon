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

import typing

import numpy as np
import pandas as pd

from pycanon import aux_functions as utils


def calculate_k(data: pd.DataFrame, quasi_ident: typing.List) -> int:
    """Calculate k for k-anonymity.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :return: k value for k-anonymity.
    :rtype: int.
    """

    utils.check_qi(data, quasi_ident)

    equiv_class = utils.get_equiv_class(data, quasi_ident)
    k_anon = min([len(x) for x in equiv_class])
    return k_anon


def calculate_l(data: pd.DataFrame,
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
    utils.check_qi(data, quasi_ident)
    utils.check_sa(data, sens_att)

    equiv_class = utils.get_equiv_class(data, quasi_ident)
    l_div = []
    if gen:
        for ec in equiv_class:
            data_temp = data.iloc[utils.convert(ec)]
            l_sa = [len(np.unique(data_temp[sa].values)) for sa in sens_att]
            l_div.append(min(l_sa))
    else:
        for i, sa in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            equiv_class = utils.get_equiv_class(data, tmp_qi)
            l_ec = []
            for ec in equiv_class:
                data_temp = data.iloc[utils.convert(ec)]
                l_ec.append(len(np.unique(data_temp[sa].values)))
            l_div.append(min(l_ec))
    return min(l_div)


def achieve_l_diversity(data: pd.DataFrame,
                        quasi_ident: typing.List,
                        sens_att: typing.List,
                        l_new: int) -> pd.DataFrame:
    """Given l, transform the dataset into a new one checking l-diversity for
    the new l, only using suppression.

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
    utils.check_qi(data, quasi_ident)
    utils.check_sa(data, sens_att)
    equiv_class = utils.get_equiv_class(data, quasi_ident)
    l_ec = []
    for ec in equiv_class:
        data_temp = data.iloc[utils.convert(ec)]
        l_sa = [len(np.unique(data_temp[sa].values)) for sa in sens_att]
        l_ec.append(min(l_sa))
    data_ec_l = pd.DataFrame({'equiv_class': equiv_class, 'l_ec': l_ec})
    data_ec_l = data_ec_l[data_ec_l.l_ec < l_new]
    ec_elim = np.concatenate([utils.convert(x)
                             for x in data_ec_l.equiv_class.values])
    data_new = data.drop(ec_elim).reset_index()
    data_new.drop('index', inplace=True, axis=1)
    return data_new


def calculate_entropy_l(data: pd.DataFrame,
                        quasi_ident: typing.List,
                        sens_att: typing.List,
                        gen=True) -> float:
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
    utils.check_qi(data, quasi_ident)
    utils.check_sa(data, sens_att)

    if gen:
        equiv_class = utils.get_equiv_class(data, quasi_ident)
        entropy_ec = []
        for ec in equiv_class:
            data_temp = data.iloc[utils.convert(ec)]
            entropy_sa = []
            for sa in sens_att:
                values = np.unique(data_temp[sa].values)
                p = [len(data_temp[data_temp[sa] == s])/len(data_temp)
                     for s in values]
                entropy = np.sum(p * np.log(p))
                entropy_sa.append(-entropy)
            entropy_ec.append(min(entropy_sa))
        ent_l = int(min(np.exp(1)**entropy_ec))
    else:
        entropy_sa = []
        for i, sa in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            equiv_class = utils.get_equiv_class(data, tmp_qi)
            entropy_ec = []
            for ec in equiv_class:
                data_temp = data.iloc[utils.convert(ec)]
                entropy = 0
                for s in np.unique(data_temp[sa].values):
                    p = len(data_temp[data_temp[sa] == s])/len(data_temp)
                    entropy += p*np.log(p)
                entropy_ec.append(-entropy)
            entropy_sa.append(min(entropy_ec))
        ent_l = int(min(np.exp(1)**entropy_sa))
    return ent_l


def calculate_c_l_diversity(data: pd.DataFrame,
                            quasi_ident: typing.List,
                            sens_att: typing.List,
                            imp=0,
                            gen=True) -> typing.Tuple[float, int]:
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
    utils.check_qi(data, quasi_ident)
    utils.check_sa(data, sens_att)
    l_div = calculate_l(data, quasi_ident, sens_att)
    if l_div > 1:
        c_div = []
        if gen:
            equiv_class = utils.get_equiv_class(data, quasi_ident)
            for sens_att_value in sens_att:
                c_sa = []
                for ec in equiv_class:
                    data_temp = data.iloc[utils.convert(ec)]
                    values = np.unique(data_temp[sens_att_value].values)
                    r_ec = np.sort(
                        [
                            len(data_temp[data_temp[sens_att_value] == s])
                            for s in values
                        ]
                    )
                    c_sa.append(np.floor(r_ec[0]/sum(r_ec[l_div - 1:]) + 1))
                c_div.append(int(max(c_sa)))
            c_div = max(c_div)
        else:
            for i, sa in enumerate(sens_att):
                tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
                equiv_class = utils.get_equiv_class(data, tmp_qi)
                c_sa = []
                for ec in equiv_class:
                    data_temp = data.iloc[utils.convert(ec)]
                    values = np.unique(data_temp[sa].values)
                    r_ec = np.sort([len(data_temp[data_temp[sa] == s])
                                   for s in values])
                    c_sa.append(np.floor(r_ec[0]/sum(r_ec[l_div - 1:]) + 1))
                c_div.append(int(max(c_sa)))
            c_div = max(c_div)
    else:
        if imp == 1:
            print(f'c for (c,l)-diversity cannot be calculated as l={l_div}')
        c_div = np.nan
    return c_div, l_div


def calculate_alpha_k(data: pd.DataFrame,
                      quasi_ident: typing.List,
                      sens_att: typing.List,
                      gen=True) -> typing.Tuple[float, int]:
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
    utils.check_qi(data, quasi_ident)
    utils.check_sa(data, sens_att)
    k_anon = calculate_k(data, quasi_ident)
    equiv_class = utils.get_equiv_class(data, quasi_ident)
    if gen:
        alpha_ec = []
        for ec in equiv_class:
            data_temp = data.iloc[utils.convert(ec)]
            alpha_sa = []
            for sa in sens_att:
                values = np.unique(data_temp[sa].values)
                _alpha = [len(data_temp[data_temp[sa] == s]) /
                          len(data_temp) for s in values]
                alpha_sa.append(max(_alpha))
            alpha_ec.append(max(alpha_sa))
        alpha = max(alpha_ec)
    else:
        alpha_sa = []
        for i, sa in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            equiv_class = utils.get_equiv_class(data, tmp_qi)
            alpha_ec = []
            for ec in equiv_class:
                data_temp = data.iloc[utils.convert(ec)]
                values = np.unique(data_temp[sa].values)
                _alpha = [len(data_temp[data_temp[sa] == s]) /
                          len(data_temp) for s in values]
                alpha_ec.append(max(_alpha))
            alpha_sa.append(max(alpha_ec))
        alpha = max(alpha_sa)
    return alpha, k_anon


def calculate_basic_beta(data: pd.DataFrame,
                         quasi_ident: typing.List,
                         sens_att: typing.List,
                         gen=True) -> float:
    """Calculate beta for basic beta-likeness.

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

    :return: beta value for basic beta-likeness.
    :rtype: float.
    """
    quasi_ident = np.array(quasi_ident)
    sens_att = np.array(sens_att)
    utils.check_qi(data, quasi_ident)
    utils.check_sa(data, sens_att)
    beta_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            _, dist = utils.aux_calculate_beta(data,
                                               quasi_ident,
                                               sens_att_value)
            beta_sens_att.append(max(dist))
    else:
        for i, sens_att_value in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            _, dist = utils.aux_calculate_beta(data, tmp_qi, sens_att_value)
            beta_sens_att.append(max(dist))
    beta = max(beta_sens_att)
    return beta


def calculate_enhanced_beta(data: pd.DataFrame,
                            quasi_ident: typing.List,
                            sens_att: typing.List,
                            gen=True) -> float:
    """Calculate beta for enhanced beta-likeness.

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

    :return: beta value for enhanced beta-likeness.
    :rtype: float.
    """
    quasi_ident = np.array(quasi_ident)
    sens_att = np.array(sens_att)
    utils.check_qi(data, quasi_ident)
    utils.check_sa(data, sens_att)
    beta_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            p, dist = utils.aux_calculate_beta(data,
                                               quasi_ident,
                                               sens_att_value)
            min_beta_lnp = [min(max(dist), -np.log(p_i)) for p_i in p]
            beta_sens_att.append(max(min_beta_lnp))
    else:
        for i, sens_att_value in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            p, dist = utils.aux_calculate_beta(data, tmp_qi, sens_att_value)
            min_beta_lnp = [min(max(dist), -np.log(p_i)) for p_i in p]
            beta_sens_att.append(max(min_beta_lnp))
    beta = max(beta_sens_att)
    return beta


def calculate_delta_disclosure(data: pd.DataFrame,
                               quasi_ident: typing.List,
                               sens_att: typing.List,
                               gen=True) -> float:
    """Calculate delta for delta-disclousure privacy.

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

    :return: delta value for delta-discloure privacy.
    :rtype: float.
    """
    quasi_ident = np.array(quasi_ident)
    sens_att = np.array(sens_att)
    utils.check_qi(data, quasi_ident)
    utils.check_sa(data, sens_att)
    delta_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            aux = utils.aux_calculate_delta_disclosure(
                data, quasi_ident, sens_att_value)
            delta_sens_att.append(max(aux))
    else:
        for i, sens_att_value in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            aux = utils.aux_calculate_delta_disclosure(data,
                                                       tmp_qi,
                                                       sens_att_value)
            delta_sens_att.append(max(aux))
    delta = max(delta_sens_att)
    return delta


def calculate_t_closeness(data: pd.DataFrame,
                          quasi_ident: typing.List,
                          sens_att: typing.List,
                          gen=True) -> float:
    """Calculate t for t-closeness.

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

    :return: t value for basic t-closeness.
    :rtype: float.
    """
    quasi_ident = np.array(quasi_ident)
    sens_att = np.array(sens_att)
    utils.check_qi(data, quasi_ident)
    utils.check_sa(data, sens_att)
    t_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            if pd.api.types.is_numeric_dtype(data[sens_att_value]):
                t_sens_att.append(utils.aux_t_closeness_num(
                    data, quasi_ident, sens_att_value))
            elif pd.api.types.is_string_dtype(data[sens_att_value]):
                t_sens_att.append(utils.aux_t_closeness_str(
                    data, quasi_ident, sens_att_value))
            else:
                raise ValueError('Error, invalid sens_att value type')
    else:
        for i, sens_att_value in enumerate(sens_att):
            if pd.api.types.is_numeric_dtype(data[sens_att_value]):
                tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
                t_sens_att.append(utils.aux_t_closeness_num(
                    data, tmp_qi, sens_att_value))
            elif pd.api.types.is_string_dtype(data[sens_att_value]):
                tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
                t_sens_att.append(utils.aux_t_closeness_str(
                    data, tmp_qi, sens_att_value))
            else:
                raise ValueError('Error, invalid sens_att value type')
    return max(t_sens_att)

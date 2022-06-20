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

from pycanon.anonymity.utils import aux_anonymity
from pycanon.anonymity.utils import aux_functions

from typing import Tuple, Any


def calculate_k(file_name: str, quasi_ident: list) -> int:
    """Calculate k for k-anonymity.

    :param file_name: name of the file with the data under study.
    :type file_name: string with csv, xlsx, sav or txt extension, or pandas 
        dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :return: k value for k-anonymity.
    :rtype: int.
    """
    if isinstance(file_name, pd.DataFrame):
        data = file_name
    else:
        data = aux_functions.read_file(file_name)
    aux_functions.check_qi(data, quasi_ident)
    equiv_class = aux_anonymity.get_equiv_class(data, quasi_ident)
    k_anon = min([len(x) for x in equiv_class])
    return k_anon


def calculate_l(
    file_name: str, quasi_ident: list, sens_att: list, gen=True) -> int:
    """Calculate l for l-diversity.

    :param file_name: name of the file with the data under study.
    :type file_name: string with csv, xlsx, sav or txt extension, or pandas 
        dataframe

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
    if isinstance(file_name, pd.DataFrame):
        data = file_name
    else:
        data = aux_functions.read_file(file_name)
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
        sens_att_array = np.array(sens_att)
        for i, sa in enumerate(sens_att_array):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att_array, i)])
            equiv_class = aux_anonymity.get_equiv_class(data, tmp_qi)
            l_ec = []
            for ec in equiv_class:
                data_temp = data.iloc[aux_functions.convert(ec)]
                l_ec.append(len(np.unique(data_temp[sa].values)))
            l_div.append(min(l_ec))
    return min(l_div)


def achieve_l_diversity(
    file_name: str, quasi_ident: list, sens_att: list, l_new: int) -> pd.DataFrame:
    """Given l, transform the dataset into a new one checking l-diversity for
    the new l, only using suppression.

    :param file_name: name of the file with the data under study.
    :type file_name: string with csv, xlsx, sav or txt extension, or pandas 
        dataframe

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
    if isinstance(file_name, pd.DataFrame):
        data = file_name
    else:
        data = aux_functions.read_file(file_name)
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)
    equiv_class = aux_anonymity.get_equiv_class(data, quasi_ident)
    l_ec = []
    for ec in equiv_class:
        data_temp = data.iloc[aux_functions.convert(ec)]
        l_sa = [len(np.unique(data_temp[sa].values)) for sa in sens_att]
        l_ec.append(min(l_sa))
    data_ec_l = pd.DataFrame({'equiv_class': equiv_class, 'l_ec': l_ec})
    data_ec_l = data_ec_l[data_ec_l.l_ec < l_new]
    ec_elim = np.concatenate([aux_functions.convert(x)
                             for x in data_ec_l.equiv_class.values])
    data_new = data.drop(ec_elim).reset_index()
    data_new.drop('index', inplace=True, axis=1)
    return data_new


def calculate_entropy_l(
    file_name: str, quasi_ident: list, sens_att: list, gen=True) -> float:
    """Calculate l for entropy l-diversity.

    :param file_name: name of the file with the data under study.
    :type file_name: string with csv, xlsx, sav or txt extension, or pandas 
        dataframe

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
    if isinstance(file_name, pd.DataFrame):
        data = file_name
    else:
        data = aux_functions.read_file(file_name)
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
                p_list = [len(data_temp[data_temp[sa] == s])/len(data_temp)
                     for s in values]
                entropy = np.sum(p_list * np.log(p_list))
                entropy_sa.append(-entropy)
            entropy_ec.append(min(entropy_sa))
        ent_l = int(min(np.exp(1)**entropy_ec))
    else:
        sens_att_array = np.array(sens_att)
        entropy_sa = []
        for i, sa in enumerate(sens_att_array):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att_array, i)])
            equiv_class = aux_anonymity.get_equiv_class(data, tmp_qi)
            entropy_ec = []
            for ec in equiv_class:
                data_temp = data.iloc[aux_functions.convert(ec)]
                entropy = 0.0
                for s in np.unique(data_temp[sa].values):
                    p = len(data_temp[data_temp[sa] == s])/len(data_temp)
                    entropy += p*np.log(p)
                entropy_ec.append(-entropy)
            entropy_sa.append(min(entropy_ec))
        ent_l = int(min(np.exp(1)**entropy_sa))
    return ent_l


def calculate_c_l_diversity(
    file_name: str, quasi_ident: list, sens_att: list, imp=0, gen=True) -> Tuple[Any, int]:
    """Calculate c and l for recursive (c,l)-diversity.

    :param file_name: name of the file with the data under study.
    :type file_name: string with csv, xlsx, sav or txt extension, or pandas 
        dataframe

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
    :rtype: c is an int and l is an int.
    """
    if isinstance(file_name, pd.DataFrame):
        data = file_name
    else:
        data = aux_functions.read_file(file_name)
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)
    l_div = calculate_l(file_name, quasi_ident, sens_att)
    if l_div > 1:
        c_div_list = []
        if gen:
            equiv_class = aux_anonymity.get_equiv_class(data, quasi_ident)
            for sens_att_value in sens_att:
                c_sa = []
                for ec in equiv_class:
                    data_temp = data.iloc[aux_functions.convert(ec)]
                    values = np.unique(data_temp[sens_att_value].values)
                    r_ec = np.sort(
                        [
                            len(data_temp[data_temp[sens_att_value] == s])
                            for s in values
                        ]
                    )
                    c_sa.append(np.floor(r_ec[0]/sum(r_ec[l_div - 1:]) + 1))
                c_div_list.append(int(max(c_sa)))
            c_div = max(c_div_list)
        else:
            sens_att_array = np.array(sens_att)
            for i, sa in enumerate(sens_att):
                tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att_array, i)])
                equiv_class = aux_anonymity.get_equiv_class(data, tmp_qi)
                c_sa = []
                for ec in equiv_class:
                    data_temp = data.iloc[aux_functions.convert(ec)]
                    values = np.unique(data_temp[sa].values)
                    r_ec = np.sort([len(data_temp[data_temp[sa] == s])
                                   for s in values])
                    c_sa.append(np.floor(r_ec[0]/sum(r_ec[l_div - 1:]) + 1))
                c_div_list.append(int(max(c_sa)))
            c_div = max(c_div_list)
    else:
        if imp == 1:
            print(f'c for (c,l)-diversity cannot be calculated as l={l_div}')
        return np.nan, 1
    return c_div, l_div


def calculate_alpha_k(
    file_name: str, quasi_ident: list, sens_att: list, gen=True) -> Tuple[float, int]:
    """Calculate alpha and k for (alpha,k)-anonymity.

    :param file_name: name of the file with the data under study.
    :type file_name: string with csv, xlsx, sav or txt extension, or pandas 
        dataframe

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
    if isinstance(file_name, pd.DataFrame):
        data = file_name
    else:
        data = aux_functions.read_file(file_name)
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)
    k_anon = calculate_k(data, quasi_ident)
    equiv_class = aux_anonymity.get_equiv_class(data, quasi_ident)
    if gen:
        alpha_ec = []
        for ec in equiv_class:
            data_temp = data.iloc[aux_functions.convert(ec)]
            alpha_sa = []
            for sa in sens_att:
                values = np.unique(data_temp[sa].values)
                _alpha = [len(data_temp[data_temp[sa] == s]) /
                          len(data_temp) for s in values]
                alpha_sa.append(max(_alpha))
            alpha_ec.append(max(alpha_sa))
        alpha = max(alpha_ec)
    else:
        sens_att_array = np.array(sens_att)
        alpha_sa = []
        for i, sa in enumerate(sens_att_array):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att_array, i)])
            equiv_class = aux_anonymity.get_equiv_class(data, tmp_qi)
            alpha_ec = []
            for ec in equiv_class:
                data_temp = data.iloc[aux_functions.convert(ec)]
                values = np.unique(data_temp[sa].values)
                _alpha = [len(data_temp[data_temp[sa] == s]) /
                          len(data_temp) for s in values]
                alpha_ec.append(max(_alpha))
            alpha_sa.append(max(alpha_ec))
        alpha = max(alpha_sa)
    return alpha, k_anon


def calculate_basic_beta(
    file_name: str, quasi_ident: list, sens_att: list, gen=True) -> float:
    """Calculate beta for basic beta-likeness.

    :param file_name: name of the file with the data under study.
    :type file_name: string with csv, xlsx, sav or txt extension, or pandas 
        dataframe

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
    if isinstance(file_name, pd.DataFrame):
        data = file_name
    else:
        data = aux_functions.read_file(file_name)
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)
    beta_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            _, dist = aux_anonymity.aux_calculate_beta(data,
                                               quasi_ident,
                                               sens_att_value)
            beta_sens_att.append(max(dist))
    else:
        sens_att_array = np.array(sens_att)
        for i, sens_att_value in enumerate(sens_att_array):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att_array, i)])
            _, dist = aux_anonymity.aux_calculate_beta(data, tmp_qi, sens_att_value)
            beta_sens_att.append(max(dist))
    beta = max(beta_sens_att)
    return beta


def calculate_enhanced_beta(
    file_name: str, quasi_ident: list, sens_att: list, gen=True) -> float:
    """Calculate beta for enhanced beta-likeness.

    :param file_name: name of the file with the data under study.
    :type file_name: string with csv, xlsx, sav or txt extension, or pandas 
        dataframe

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
    if isinstance(file_name, pd.DataFrame):
        data = file_name
    else:
        data = aux_functions.read_file(file_name)
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)
    beta_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            p, dist = aux_anonymity.aux_calculate_beta(data,
                                               quasi_ident,
                                               sens_att_value)
            min_beta_lnp = [min(max(dist), -np.log(p_i)) for p_i in p]
            beta_sens_att.append(max(min_beta_lnp))
    else:
        sens_att_array = np.array(sens_att)
        for i, sens_att_value in enumerate(sens_att_array):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att_array, i)])
            p, dist = aux_anonymity.aux_calculate_beta(data, tmp_qi, sens_att_value)
            min_beta_lnp = [min(max(dist), -np.log(p_i)) for p_i in p]
            beta_sens_att.append(max(min_beta_lnp))
    beta = max(beta_sens_att)
    return beta


def calculate_delta_disclosure(
    file_name: str, quasi_ident: list, sens_att: list, gen=True) -> float:
    """Calculate delta for delta-disclousure privacy.

    :param file_name: name of the file with the data under study.
    :type file_name: string with csv, xlsx, sav or txt extension, or pandas 
        dataframe

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
    if isinstance(file_name, pd.DataFrame):
        data = file_name
    else:
        data = aux_functions.read_file(file_name)
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)
    delta_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            aux = aux_anonymity.aux_calculate_delta_disclosure(
                data, quasi_ident, sens_att_value)
            delta_sens_att.append(aux)
    else:
        sens_att_array = np.array(sens_att)
        for i, sens_att_value in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att_array, i)])
            aux = aux_anonymity.aux_calculate_delta_disclosure(data,
                                                       tmp_qi,
                                                       sens_att_value)
            delta_sens_att.append(aux)
    delta = max(delta_sens_att)
    return delta


def calculate_t_closeness(
    file_name: str, quasi_ident: list, sens_att: list, gen=True) -> float:
    """Calculate t for t-closeness.

    :param file_name: name of the file with the data under study.
    :type file_name: string with csv, xlsx, sav or txt extension, or pandas 
        dataframe

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
    if isinstance(file_name, pd.DataFrame):
        data = file_name
    else:
        data = aux_functions.read_file(file_name)
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)
    t_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            if pd.api.types.is_numeric_dtype(data[sens_att_value]):
                t_sens_att.append(aux_anonymity.aux_t_closeness_num(
                    data, quasi_ident, sens_att_value))
            elif pd.api.types.is_string_dtype(data[sens_att_value]):
                t_sens_att.append(aux_anonymity.aux_t_closeness_str(
                    data, quasi_ident, sens_att_value))
            else:
                raise ValueError('Error, invalid sens_att value type')
    else:
        sens_att_array = np.array(sens_att)
        for i, sens_att_value in enumerate(sens_att_array):
            if pd.api.types.is_numeric_dtype(data[sens_att_value]):
                tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att_array, i)])
                t_sens_att.append(aux_anonymity.aux_t_closeness_num(
                    data, tmp_qi, sens_att_value))
            elif pd.api.types.is_string_dtype(data[sens_att_value]):
                tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att_array, i)])
                t_sens_att.append(aux_anonymity.aux_t_closeness_str(
                    data, tmp_qi, sens_att_value))
            else:
                raise ValueError('Error, invalid sens_att value type')
    return max(t_sens_att)

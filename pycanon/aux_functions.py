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

import os

import numpy as np
import pandas as pd


def read_file(file_name):
    """Read the given file. Returns a pandas dataframe.

    :param file_name: name of the file with the data under study.
    :type file_name: string with csv, xlsx, sav or txt extension.

    :return: dataframe with the data.
    :rtype: pandas dataframe.
    """
    _, file_extension = os.path.splitext(file_name)
    if file_extension in ['.csv', '.xlsx', '.sav', '.txt']:
        if file_extension in ['.csv', '.txt']:
            data = pd.read_csv(file_name)
        elif file_extension == '.xlsx':
            data = pd.read_excel(file_name)
        else:
            data = pd.read_spss(file_name)
    else:
        raise ValueError('Invalid file extension.')
    return data


def check_qi(data, quasi_ident):
    """Checks if the entered quasi-identifiers are valid.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings
    """
    cols = data.columns
    err_val = [i for i, v in enumerate(
        [qi in cols for qi in quasi_ident]) if v is False]
    if len(err_val) > 0:
        raise ValueError(
            f'Values not defined: {[quasi_ident[i] for i in err_val]}. '
            'Cannot be quasi-identifiers'
        )


def check_sa(data, sens_att):
    """Checks if the entered sensitive attributes are valid.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: is a list of strings.
    """
    cols = data.columns
    err_val = [i for i, v in enumerate(
        [sa in cols for sa in sens_att]) if v is False]
    if len(err_val) > 0:
        raise ValueError(
            f'Values not defined: {[sens_att[i] for i in err_val]}. '
            'Cannot be sensitive attributes')


def get_equiv_class(data, quasi_ident):
    """Find the equivalence classes present in the dataset.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: is a list of strings
    """
    index = []
    for qi in quasi_ident:
        values = np.unique(data[qi].values)
        tmp = [np.unique(data[data[qi] == value].index) for value in values]
        index.append(tmp)
    index = sorted(index, key=lambda x: len(x))
    equiv_class = index.copy()
    while len(equiv_class) > 1:
        equiv_class = intersect(equiv_class)
        equiv_class = sorted(equiv_class, key=lambda x: len(x))
    equiv_class = [x for x in equiv_class[0] if len(x) > 0]
    return equiv_class


def intersect(tmp):
    """Intersect two sets: the first and the second of the given list.

    :param tmp: list of sets sorted in decreasing order of
        cardinality
    :type tmp: list of numpy arrays.
    """
    i, j = 0, 0
    tmp_new = []
    while i < len(tmp[0]):
        tmp1 = tmp[0][i]
        tmp2 = tmp[1][j]
        tmp_new.append(np.intersect1d(tmp1, tmp2))
        if j < len(tmp[1])-1:
            j += 1
        else:
            j = 0
            i += 1
    tmp[1] = tmp_new
    tmp = tmp[1:]
    return tmp


def convert(ec_set):
    """Converts a set with an equivalence class to a list.

    :param ec_set: set which will be convert into a list.
    :type ec_set: set.
    """
    return [*ec_set, ]


def aux_calculate_beta(data, quasi_ident, sens_att_value):
    """Beta calculation for basic and enhanced beta-likeness.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: list of strings
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    p = np.array([len(data[data[sens_att_value] == s])/len(data)
                 for s in values])
    q = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        qi = np.array(
            [
                len(data_temp[data_temp[sens_att_value] == s]) / len(ec)
                for s in values
            ]
        )
        q.append(qi)
    dist = [max((q[i]-p)/p) for i in range(len(equiv_class))]
    return p, dist


def aux_calculate_delta_disclosure(data, quasi_ident, sens_att_value):
    """Delta calculation for delta-disclousure privacy.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: list of strings
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    p = np.array([len(data[data[sens_att_value] == s])/len(data)
                 for s in values])
    q = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        qi = np.array(
            [
                len(data_temp[data_temp[sens_att_value] == s]) / len(ec)
                for s in values
            ]
        )
        q.append(qi)
    aux = [max([np.abs(np.log(x)) for x in qi/p if x > 0]) for qi in q]
    return aux


def aux_t_closeness_num(data, quasi_ident, sens_att_value):
    """t calculation for t-closeness.

    Function used for numerical attributes: the definition of the EMD is used.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: list of strings
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    m = len(values)
    p = np.array([len(data[data[sens_att_value] == s])/len(data)
                 for s in values])
    emd = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        qi = np.array(
            [
                len(data_temp[data_temp[sens_att_value] == s]) / len(ec)
                for s in values
            ]
        )
        r = qi - p
        abs_r, emd_ec = 0, 0
        for i in range(m):
            abs_r += r[i]
            emd_ec += np.abs(abs_r)
        emd_ec = 1/(m-1) * emd_ec
        emd.append(emd_ec)
    return max(emd)


def aux_t_closeness_str(data, quasi_ident, sens_att_value):
    """t calculation for t-closeness.

    Function used for categorical attributes: the metric "Equal Distance" is
    used.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: list of strings
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    m = len(values)
    p = np.array([len(data[data[sens_att_value] == s])/len(data)
                 for s in values])
    emd = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        qi = np.array(
            [
                len(data_temp[data_temp[sens_att_value] == s]) / len(ec)
                for s in values
            ]
        )
        r = qi - p
        emd_ec = 0
        for i in range(m):
            emd_ec += np.abs(r[i])
        emd_ec = 0.5 * emd_ec
        emd.append(emd_ec)
    return max(emd)

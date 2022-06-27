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

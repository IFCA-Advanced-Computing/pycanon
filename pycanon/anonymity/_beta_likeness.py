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


def basic_beta_likeness(
    data: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: typing.Union[typing.List, np.ndarray],
    gen=True,
) -> float:
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
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)
    beta_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            _, dist = aux_anonymity.aux_calculate_beta(
                data, quasi_ident, sens_att_value
            )
            beta_sens_att.append(max(dist))
    else:
        for i, sens_att_value in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            _, dist = aux_anonymity.aux_calculate_beta(data, tmp_qi, sens_att_value)
            beta_sens_att.append(max(dist))
    beta = max(beta_sens_att)
    return beta


def enhanced_beta_likeness(
    data: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: typing.Union[typing.List, np.ndarray],
    gen=True,
) -> float:
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
    aux_functions.check_qi(data, quasi_ident)
    aux_functions.check_sa(data, sens_att)
    beta_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            p, dist = aux_anonymity.aux_calculate_beta(
                data, quasi_ident, sens_att_value
            )
            min_beta_lnp = [min(max(dist), -np.log(p_i)) for p_i in p]
            beta_sens_att.append(max(min_beta_lnp))
    else:
        for i, sens_att_value in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            p, dist = aux_anonymity.aux_calculate_beta(data, tmp_qi, sens_att_value)
            min_beta_lnp = [min(max(dist), -np.log(p_i)) for p_i in p]
            beta_sens_att.append(max(min_beta_lnp))
    beta = max(beta_sens_att)
    return beta

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
from pycanon import anonymity
from pycanon.anonymity.utils import aux_anonymity


def average_ecsize(
    data_raw: pd.DataFrame,
    data_anon: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sup=True,
) -> float:
    """Calculate the metric average equivalence class size.

    :param data_raw: dataframe with the data raw under study.
    :type data_raw: pandas dataframe

    :param data_anon: dataframe with the data anonymized.
    :type data_anon: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
            that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sup: boolean, default to True. If true, suppression has been applied to the
        original dataset (some records may have been deleted).
    :type  sup: boolean
    """
    equiv_class = aux_anonymity.get_equiv_class(data_anon, quasi_ident)
    k = anonymity.k_anonymity(data_anon, quasi_ident)
    if sup:
        return len(data_anon) / (len(equiv_class) * k)
    return len(data_raw) / (len(equiv_class) * k)


def classification_metric(
    data_raw: pd.DataFrame,
    data_anon: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: typing.Union[typing.List, np.ndarray],
) -> float:
    """Calculate the classification metric.

    :param data_raw: dataframe with the data raw under study.
    :type data_raw: pandas dataframe

    :param data_anon: dataframe with the data anonymized.
    :type data_anon: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
            that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: list of strings
    """
    equiv_class = aux_anonymity.get_equiv_class(data_anon, quasi_ident)
    cm = len(data_raw) - len(data_anon)
    for ec in equiv_class:
        sa_ec = data_anon.iloc[ec, :][sens_att].values
        _, counts = np.unique(sa_ec, return_counts=True)
        for i in counts:
            if i != max(counts):
                cm += i
    return cm / len(data_raw)


def discernability_metric(
    data_raw: pd.DataFrame,
    data_anon: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
) -> float:
    """Calculate the discernability metric.

    :param data_raw: dataframe with the data raw under study.
    :type data_raw: pandas dataframe

    :param data_anon: dataframe with the data anonymized. Assuming that all the
    equivalence classes have more than k records, and given each suppressed record
    a penalty of the size of the input dataset.
    :type data_anon: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
                that are quasi-identifiers.
    :type quasi_ident: list of strings
    """
    equiv_class = aux_anonymity.get_equiv_class(data_anon, quasi_ident)
    dm = sum(len(ec) ** 2 for ec in equiv_class)
    supp_rec = len(data_raw) - len(data_anon)
    dm += supp_rec * len(data_raw)
    return dm

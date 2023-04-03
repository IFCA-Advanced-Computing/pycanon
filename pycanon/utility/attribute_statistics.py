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


def sizes_ec(
    data: pd.DataFrame, quasi_ident: typing.Union[typing.List, np.ndarray]
) -> dict:
    """Calculate statistics associated to the equivalence classes.

    :param data: dataframe with the data anonymized.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
            that are quasi-identifiers.
    :type quasi_ident: list of strings
    """
    equiv_class = aux_anonymity.get_equiv_class(data, quasi_ident)
    len_ec = [len(ec) for ec in equiv_class]
    stats_ec = {
        "n_ec": len(equiv_class),
        "min_ec": min(len_ec),
        "max_ec": max(len_ec),
        "mean_ec": np.mean(len_ec),
        "median_ec": np.median(len_ec),
    }
    return stats_ec


def stats_quasi_ident(data: pd.DataFrame, quasi_ident: str) -> dict:
    """Calculate statistics associated to a given quasi-identifier.

    :param data: dataframe with the data anonymized.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
            that are quasi-identifiers.
    :type quasi_ident: list of strings
    """
    qi_values = data[quasi_ident].values
    values, counts = np.unique(qi_values, return_counts=True)
    stats_qi = {
        "max_freq_value": np.mode(qi_values),
        "max_freq": max(counts),
        "min_freq_value": values[np.argmin(counts)],
        "min_freq": min(counts),
    }
    if isinstance(qi_values[0], (int, float)):
        stats_qi["mean"] = np.mean(qi_values)
        stats_qi["median"] = np.median(qi_values)
        stats_qi["std"] = np.std(qi_values)
        stats_qi["var"] = np.var(qi_values)
    return stats_qi

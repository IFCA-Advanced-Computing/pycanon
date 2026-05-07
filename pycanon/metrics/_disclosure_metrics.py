# -*- coding: utf-8 -*-

# Copyright 2025 Spanish National Research Council (CSIC)
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

import numpy as np
import pandas as pd
from scipy.stats import entropy
from pycanon.anonymity.utils import aux_functions


def sa_entropy(data_anon: pd.DataFrame, sens_attr: str) -> float:
    """Calculate Shannon Entropy for a sensitive attribute.

    :param data_anon: dataframe with the data anonymized.
    :type data_anon: pandas dataframe

    :param sens_attr: string with the senstive attribute for calculating the entropy.
    :type sens_attr: string

    :return: Shannon entropy for the sensitive attribute.
    :rtype: float
    """
    aux_functions.check_sa(data_anon, [sens_attr])
    pk = []
    n_records = len(data_anon)
    for value in data_anon[sens_attr].values:
        pk.append(len(data_anon[sens_attr == value]) / n_records)
    return entropy(pk)

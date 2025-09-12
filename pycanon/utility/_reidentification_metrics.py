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

import typing
import numpy as np
import pandas as pd
from pycanon import anonymity
from pycanon.anonymity.utils import aux_anonymity

def average_rir(
        data_anon: pd.DataFrame,
        quasi_ident: typing.Union[typing.List, np.ndarray]
) -> float:
    """ Calculate the average re-identification risk metric

    :param data_anon: dataframe with the data anonymized.
    :type data_anon: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
            that are quasi-identifiers.
    :type quasi_ident: list of strings
    """
    equiv_class = aux_anonymity.get_equiv_class(data_anon, quasi_ident)
    avg_rir = np.mean([1/len(ec) for ec in equiv_class])
    return avg_rir

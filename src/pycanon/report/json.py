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

"""Get report values as JSON for all privacy models."""

import json
import typing

import numpy as np
import pandas as pd

from pycanon.report import base


class _NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(_NpEncoder, self).default(obj)


def get_json_report(
    data: pd.DataFrame, quasi_ident: list, sens_att: list, gen=True
) -> str:
    """Generate a report (JSON) with the parameters obtained for each anonymity check.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: is a list of strings

    :param gen: default to true. If true it is generalized for the case of
        multiple SA, if False, the set of QI is updated for each SA.
    :type gen: boolean
    """
    (
        k_anon,
        (alpha, alpha_k),
        l_div,
        entropy_l,
        (c_div, l_c_div),
        basic_beta,
        enhanced_beta,
        delta_disc,
        t_clos,
    ) = base.get_report_values(data, quasi_ident, sens_att, gen=gen)

    json_data: typing.Dict[str, typing.Any] = {
        "data": {"quasi-identifiers": quasi_ident, "sensitive attributes": sens_att},
        "k_anonymity": {"k": k_anon},
        "alpha_k_anonymity": {"alpha": alpha, "k": alpha_k},
        "l_diversity": {"l": l_div},
        "entropy_l_diversity": {"l": entropy_l},
        "recursive_c_l_diversity": {"c": c_div, "l": l_c_div},
        "basic_beta_likeness": {"beta": basic_beta},
        "enhanced_beta_likeness": {"beta": enhanced_beta},
        "t_closeness": {"t": t_clos},
        "delta_disclosure": {"delta": delta_disc},
    }

    return json.dumps(json_data, cls=_NpEncoder)

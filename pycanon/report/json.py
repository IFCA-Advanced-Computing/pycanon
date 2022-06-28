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

import pandas as pd
import json

from pycanon.report import base
from typing import Union


def get_json_report(file_name: Union[str, pd.DataFrame], quasi_ident: list, sens_att: list, gen=True) -> json:
    """Generate a report with the parameters obtained for each anonymity check.

    :param file_name: name of the file with the data under study or pandas
        dataframe.
    :type file_name: string with csv, xlsx, sav or txt extension or
        pandas dataframe

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
        k_anon, (alpha, alpha_k), l_div, entropy_l, (c_div, l_c_div),
        basic_beta, enhanced_beta, delta_disc, t_clos
    ) = base.get_report_values(file_name, quasi_ident, sens_att, gen=gen)

    json_data = {}
    json_data['data'] = {
        'file': file_name,
        'quasi-identifiers': quasi_ident,
        'sensitive attributes': sens_att
    }
    json_data['k_anonymity'] = {'k': k_anon}
    json_data['alpha_k_anonymity'] = {'alpha': alpha, 'k': alpha_k}
    json_data['l_diversity'] = {'l': l_div}
    json_data['entropy_l_diversity'] = {'l': entropy_l}
    json_data['recursive_c_l_diversity'] = {'c': c_div, 'l': l_c_div}
    json_data['basic_beta_likeness'] = {'beta': basic_beta}
    json_data['enhanced_beta_likeness'] = {'beta': enhanced_beta}
    json_data['t_closeness'] = {'t': t_clos}
    json_data['delta_disclosure'] = {'delta': delta_disc}

    return json.dumps(json_data)

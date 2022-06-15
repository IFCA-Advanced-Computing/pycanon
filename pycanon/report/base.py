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

from pycanon import anonymity
from pycanon import aux_functions as utils


def get_report_values(file_name, quasi_ident, sens_att, gen=True):
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
    data = utils.read_file(file_name)

    k_anon = anonymity.calculate_k(
        data, quasi_ident
    )
    alpha, alpha_k = anonymity.calculate_alpha_k(
        data, quasi_ident, sens_att, gen
    )
    l_div = anonymity.calculate_l(
        data, quasi_ident, sens_att, gen
    )
    entropy_l = anonymity.calculate_entropy_l(
        data, quasi_ident, sens_att, gen
    )
    c_div, l_c_div = anonymity.calculate_c_l_diversity(
        data, quasi_ident, sens_att, gen
    )
    basic_beta = anonymity.calculate_basic_beta(
        data, quasi_ident, sens_att, gen
    )
    enhanced_beta = anonymity.calculate_enhanced_beta(
        data, quasi_ident, sens_att, gen
    )
    delta_disc = anonymity.calculate_delta_disclosure(
        data, quasi_ident, sens_att, gen
    )
    t_clos = anonymity.calculate_t_closeness(
        data, quasi_ident, sens_att, gen
    )

    # TODO(aloga): Move to a better data type here
    return (k_anon, (alpha, alpha_k), l_div, entropy_l, (c_div, l_c_div),
            basic_beta, enhanced_beta, delta_disc, t_clos)

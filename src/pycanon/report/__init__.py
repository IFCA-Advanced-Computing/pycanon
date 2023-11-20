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

"""Generate reports with all privacy model's scores."""

import pandas as pd

from pycanon.report.base import get_report_values  # noqa(F401)
from pycanon.report.json import get_json_report  # noqa(F401)

try:
    from pycanon.report.pdf import get_pdf_report  # noqa(F401)
    from pycanon.report.pdf_utility_report import get_pdf_utility_report  # noqa(F401)
except ImportError:
    __all_pdf__ = []
else:
    __all_pdf__ = [
        "get_pdf_report",
        "get_pdf_utility_report",
    ]


def print_report(
    data: pd.DataFrame, quasi_ident: list, sens_att: list, gen=True
) -> None:
    """Generate a report with the parameters obtained for each anonymity check.

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
    ) = get_report_values(data, quasi_ident, sens_att, gen=gen)

    print(
        f"""The dataset verifies:
          \t - k-anonymity with k = {k_anon}
          \t - (alpha,k)-anonymity with alpha = {alpha} and k = {k_anon}
          \t - l-diversity with l = {l_div}
          \t - entropy l-diversity with l = {entropy_l}
          \t - (c,l)-diversity with c = {c_div} and l = {l_div}
          \t - basic beta-likeness with beta = {basic_beta}
          \t - enhanced beta-likeness with beta = {enhanced_beta}
          \t - t-closeness with t = {t_clos}
          \t - delta-disclosure privacy with delta = {delta_disc}"""
    )


__all__ = [
    "print_report",
    "get_json_report",
    "get_report_values",
] + __all_pdf__

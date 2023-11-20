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

"""Get utility report values."""

import os
import typing
from datetime import datetime
import numpy as np
import pandas as pd
from pycanon import utility
from pycanon.report import base
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tables import Table
from reportlab.lib import colors


def get_utility_report_values(
    data_raw: pd.DataFrame,
    data_anon: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: typing.Union[typing.List, np.ndarray],
    sup=True,
) -> typing.Tuple[float, float, float, dict]:
    """Generate a report with the parameters obtained for each utility metric.

    :param data_raw: dataframe with the data raw under study.
    :type data_raw: pandas dataframe

    :param data_anon: dataframe with the data anonymized.
    :type data_anon: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: is a list of strings

    :param sup: boolean, default to True. If true, suppression has been applied to the
        original dataset (somo records may have been deleted)-
    :type  sup: boolean
    """
    avg_ec = utility.average_ecsize(data_raw, data_anon, quasi_ident, sup)
    cm = utility.classification_metric(data_raw, data_anon, quasi_ident, sens_att)
    dm = utility.discernability_metric(data_raw, data_anon, quasi_ident)

    stats_ec = utility.sizes_ec(data_anon, quasi_ident)

    return avg_ec, cm, dm, stats_ec


def get_pdf_utility_report(
    data_raw: pd.DataFrame,
    data_anon: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: typing.Union[typing.List, np.ndarray],
    sup=True,
    gen=True,
    file_pdf="utility_report.pdf",
) -> None:
    """Generate the PDF report both with the utility and anonymity checks.

    :param data_raw: dataframe with the data raw under study.
    :type data_raw: pandas dataframe

    :param data_anon: dataframe with the data anonymized.
    :type data_anon: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: is a list of strings

    :param sup: boolean, default to True. If true, suppression has been applied to the
        original dataset (somo records may have been deleted)-
    :type  sup: boolean

    :param gen: default to true. If true it is generalized for the case of
        multiple SA, if False, the set of QI is updated for each SA.
    :type gen: boolean

    :param file_pdf: name of the pdf file with the report. Default to
        'report.pdf'
    :type file_pdf: string with extension .pdf
    """
    avg_ec, cm, dm, stats_ec = get_utility_report_values(
        data_raw, data_anon, quasi_ident, sens_att, sup
    )

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
    ) = base.get_report_values(data_anon, quasi_ident, sens_att, gen=True)

    _, file_extension = os.path.splitext(file_pdf)
    if file_extension != ".pdf":
        raise ValueError("Invalid file extension. Expected .pdf extension for file_pdf")
    doc = SimpleDocTemplate(
        file_pdf,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )
    story = []
    today = datetime.now()
    date = today.strftime("%b %d %Y %H:%M:%S")

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "JustifyRight11",
            fontName="Helvetica",
            fontSize=11,
            alignment=0,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            "JustifyRight11Bold",
            fontName="Helvetica-Bold",
            fontSize=11,
            alignment=0,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            "JustifyRight12BoldSpace",
            fontName="Helvetica-Bold",
            fontSize=12,
            alignment=0,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            "main_title",
            fontName="Helvetica-Bold",
            fontSize=18,
            parent=styles["Heading2"],
            alignment=1,
            spaceAfter=20,
        )
    )

    story.append(Paragraph("pyCANON: Check anonymity properties", styles["main_title"]))
    story.append(Paragraph("Anonymity and utility report", styles["main_title"]))
    story.append(Paragraph(date, styles["JustifyRight12BoldSpace"]))

    #    story.append(Paragraph(
    #        f'File (or pandas dataframe) name: {str(file_name)}',
    #        styles["JustifyRight11"])
    #    )
    story.append(
        Paragraph(f"Quasi-identifiers: {quasi_ident}", styles["JustifyRight11"])
    )
    story.append(
        Paragraph(f"Sensitive attribute(s): {sens_att}", styles["JustifyRight11"])
    )
    if len(sens_att) > 1:
        story.append(
            Paragraph(f"Approach for more than one SA: {gen}", styles["JustifyRight11"])
        )
    story.append(Spacer(1, 20))
    prop = [
        (
            Paragraph("Anonymity technique", styles["JustifyRight11Bold"]),
            Paragraph("Value(s)", styles["JustifyRight11Bold"]),
        ),
        ("k-anonymity", f"k = {k_anon}"),
        ("(α,k)-anonymity", f"α = {alpha} and k = {k_anon}"),
        ("l-diversity", f"l = {l_div}"),
        ("Entropy l-diversity", f"l = {entropy_l}"),
        ("(c,l)-diversity", f"c = {c_div} and l = {l_div}"),
        ("Basic β-likeness", f"β = {basic_beta}"),
        ("Enhanced β-likeness", f"β = {enhanced_beta}"),
        ("t-closeness", f"t = {t_clos}"),
        ("δ-disclosure privacy", f"δ = {delta_disc}"),
    ]

    story.append(
        Table(
            prop,
            style=[
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("BACKGROUND", (0, 0), (1, 0), colors.aliceblue),
            ],
        )
    )
    story.append(Spacer(1, 20))
    story.append(Paragraph("Utility models", styles["JustifyRight12BoldSpace"]))
    story.append(
        Paragraph(
            f"\t -Average equivalence class size: {avg_ec}", styles["JustifyRight11"]
        )
    )
    story.append(
        Paragraph(f"\t -Classification metric: {cm}", styles["JustifyRight11"])
    )
    story.append(
        Paragraph(f"\t -Discernability metric: {dm}", styles["JustifyRight11"])
    )
    story.append(Spacer(1, 20))
    story.append(
        Paragraph("Equivalence classes information", styles["JustifyRight12BoldSpace"])
    )
    story.append(
        Paragraph(
            f"\t -Number of equivalence classes: {stats_ec['n_ec']}",
            styles["JustifyRight11"],
        )
    )
    story.append(
        Paragraph(f"\t -Max size: {stats_ec['max_ec']}", styles["JustifyRight11"])
    )
    story.append(
        Paragraph(f"\t -Min size: {stats_ec['min_ec']}", styles["JustifyRight11"])
    )
    story.append(
        Paragraph(f"\t -Mean size: {stats_ec['mean_ec']}", styles["JustifyRight11"])
    )
    story.append(
        Paragraph(f"\t -Median size: {stats_ec['median_ec']}", styles["JustifyRight11"])
    )

    doc.build(story)

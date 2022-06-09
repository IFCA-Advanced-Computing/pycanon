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

from datetime import datetime
import json
import os

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tables import Table
from reportlab.lib import colors

from pycanon import anonymity
from pycanon import aux_functions as utils


def get_anon_report(file_name,
                    quasi_ident,
                    sens_att,
                    gen=True,
                    imp=True,
                    file_pdf=False,
                    file_json=False):
    """Generate a report with the parameters obtained for each anonymity check.

    Parameter file_name: name of the file with the data under study.
    Precondition: file_name must have csv, xlsx, sav or txt extension.
    In can also be a pandas dataframe.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.

    Parameter gen: boolean, if true, it is generalized for the case of multiple
    SA, if False, the set of QI is updated for each SA.
    Precondition: gen = True (default) or gen = False.

    Parameter imp: boolean, level of impresion. If imp = True the report is
    displayed on the command line.
    Precondition: imp = True (default) or imp = False.

    Parameter file_pdf: string with name of the pdf file with the report. False
    if just want to view the report by command line, without saving to a pdf.
    Precondition: file_pdf is a string (with extension .pdf) of is False
    (boolean).

    Parameter file_pdf: string with name of the pdf file with the report. False
    if just want to view the report by command line, without saving to a pdf.
    Precondition: file_pdf is a string (with extension .pdf) of is False
    (boolean).
    """
    data = utils.read_file(file_name)

    k_anon = anonymity.calculate_k(
        data, quasi_ident
    )
    alpha, _ = anonymity.calculate_alpha_k(
        data, quasi_ident, sens_att, gen
    )
    l_div = anonymity.calculate_l(
        data, quasi_ident, sens_att, gen
    )
    entropy_l = anonymity.calculate_entropy_l(
        data, quasi_ident, sens_att, gen
    )
    c_div, _ = anonymity.calculate_c_l_diversity(
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

    if imp:
        print(f'''File: {file_name}. The dataset verifies:
        \t - k-anonymity with k = {k_anon}
        \t - (alpha,k)-anonymity with alpha = {alpha} and k = {k_anon}
        \t - l-diversity with l = {l_div}
        \t - entropy l-diversity with l = {entropy_l}
        \t - (c,l)-diversity with c = {c_div} and l = {l_div}
        \t - basic beta-likeness with beta = {basic_beta}
        \t - enhanced beta-likeness with beta = {enhanced_beta}
        \t - t-closeness with t = {t_clos}
        \t - delta-disclosure privacy with delta = {delta_disc}''')

    if file_pdf is not False:
        _, file_extension = os.path.splitext(file_pdf)
        if file_extension != '.pdf':
            raise ValueError(
                'Invalid file extension. Expected .pdf extension for file_pdf')
        doc = SimpleDocTemplate(file_pdf, pagesize=A4,
                                rightMargin=50, leftMargin=50,
                                topMargin=50, bottomMargin=50)
        story = []
        today = datetime.now()
        date = today.strftime("%b %d %Y %H:%M:%S")

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle('JustifyRight11',
                                  fontName="Helvetica",
                                  fontSize=11,
                                  alignment=0,
                                  spaceAfter=5))
        styles.add(ParagraphStyle('JustifyRight11Bold',
                                  fontName="Helvetica-Bold",
                                  fontSize=11,
                                  alignment=0,
                                  spaceAfter=10))
        styles.add(ParagraphStyle('JustifyRight12BoldSpace',
                                  fontName="Helvetica-Bold",
                                  fontSize=12,
                                  alignment=0,
                                  spaceAfter=10))
        styles.add(ParagraphStyle('main_title',
                                  fontName="Helvetica-Bold",
                                  fontSize=18,
                                  parent=styles['Heading2'],
                                  alignment=1,
                                  spaceAfter=20))

        story.append(
            Paragraph('PyCANON: Check ANONymity properties',
                      styles["main_title"])
        )
        story.append(Paragraph('Report', styles["main_title"]))
        story.append(Paragraph(date, styles["JustifyRight12BoldSpace"]))

        story.append(Paragraph(
            f'File (or pandas dataframe) name: {str(file_name)}',
            styles["JustifyRight11"])
        )
        story.append(Paragraph(f'Quasi-identifiers: {quasi_ident}',
                               styles["JustifyRight11"]))
        story.append(Paragraph(f'Sensitive attribute(s): {sens_att}',
                               styles["JustifyRight11"]))
        if len(sens_att) > 1:
            story.append(Paragraph(f'Approach for more than one SA: {gen}',
                                   styles["JustifyRight11"]))
        story.append(Spacer(1, 20))
        prop = [(Paragraph('Anonymity property', styles["JustifyRight11Bold"]),
                 Paragraph('Value(s)', styles["JustifyRight11Bold"])),
                ('k-anonymity', f'k = {k_anon}'),
                ('(α,k)-anonymity', f'α = {alpha} and k = {k_anon}'),
                ('l-diversity', f'l = {l_div}'),
                ('Entropy l-diversity', f'l = {entropy_l}'),
                ('(c,l)-diversity', f'c = {c_div} and l = {l_div}'),
                ('Basic β-likeness', f'β = {basic_beta}'),
                ('Enhanced β-likeness', f'β = {enhanced_beta}'),
                ('t-closeness', f't = {t_clos}'),
                ('δ-disclosure privacy', f'δ = {delta_disc}')]

        story.append(
            Table(prop,
                  style=[('GRID', (0, 0), (-1, -1), 1, colors.grey),
                         ('BACKGROUND', (0, 0), (1, 0), colors.aliceblue)])
        )
        doc.build(story)

    if file_json is not False:
        json_data = {}
        json_data['data'] = {
            'file': file_name,
            'quasi-identifiers': quasi_ident,
            'sensitive attributes': sens_att
        }
        json_data['k_anonymity'] = {'k': k_anon}
        json_data['alpha_k_anonymity'] = {'alpha': alpha, 'k': k_anon}
        json_data['l_diversity'] = {'l': l_div}
        json_data['entropy_l_diversity'] = {'l': entropy_l}
        json_data['recursive_c_l_diversity'] = {'c': c_div, 'l': l_div}
        json_data['basic_beta_likeness'] = {'beta': basic_beta}
        json_data['enhanced_beta_likeness'] = {'beta': enhanced_beta}
        json_data['t_closeness'] = {'t': t_clos}
        json_data['delta_disclosure'] = {'delta': delta_disc}

        with open(file_json, 'w') as f:
            json.dump(json_data, f, indent=4)

    return (k_anon, alpha, l_div, entropy_l, c_div, basic_beta,
            enhanced_beta, delta_disc, t_clos)

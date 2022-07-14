"""Example using the drug type prediction dataset."""

import numpy as np
from pycanon import anonymity


def anonymity_level(file_name, quasi_ident, sens_att):
    """Function for check all the anonymity techniques under study."""
    k_anon = anonymity.k_anonymity(file_name, quasi_ident)
    l_div = anonymity.l_diversity(file_name, quasi_ident, sens_att)
    entropy_l = anonymity.entropy_l_diversity(file_name, quasi_ident, sens_att)
    alpha, _ = anonymity.alpha_k_anonymity(file_name, quasi_ident, sens_att)
    basic_beta = anonymity.basic_beta_likeness(file_name, quasi_ident, sens_att)
    enhanced_beta = anonymity.enhanced_beta_likeness(file_name, quasi_ident, sens_att)
    delta_disclosure = anonymity.delta_disclosure(file_name, quasi_ident, sens_att)
    t_clos = anonymity.t_closeness(file_name, quasi_ident, sens_att)
    c_div, _ = anonymity.recursive_c_l_diversity(file_name, quasi_ident, sens_att)

    print(f'''File: {file_name}. The dataset verifies:
    \t - k-anonymity with k = {k_anon}
    \t - (alpha,k)-anonymity with alpha = {alpha} and k = {k_anon}
    \t - l-diversity with l = {l_div}
    \t - entropy l-diversity with l = {entropy_l}
    \t - basic beta-likeness with beta = {basic_beta}
    \t - enhanced beta-likeness with beta = {enhanced_beta}
    \t - delta-disclosure privacy with delta = {delta_disclosure}
    \t - t-closeness with t = {t_clos}''')
    if np.isnan(c_div):
        print(f'\t - As l = {l_div} for l-diversity, c cannot be calculated for (c,l)-diversity.\n')
    else:
        print(f'\t - (c,l)-diversity with c = {c_div} and l = {l_div}.\n')


QI = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']
SA = ['Drug']
FILE_NAME = './data/processed/drug_type.csv'
anonymity_level(FILE_NAME, QI, SA)

FILE_NAME = './data/processed/drugs_k5.csv'
anonymity_level(FILE_NAME, QI, SA)

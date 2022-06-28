"""Example using the student's math score dataset."""

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


QI = ['Teacher', 'Gender', 'Ethnic', 'Freeredu', 'wesson']
FILE_NAME = './Data/Processed/StudentsMath_Score.csv'
SA = ['Score']
anonymity_level(FILE_NAME, QI, SA)

for i in [2, 5, 7]:
    FILE_NAME = f'./Data/Processed/StudentsMath_Score_k{i}.csv'
    anonymity_level(FILE_NAME, QI, SA)

"""Example using the drug type prediction dataset."""

import numpy as np
from pycanon.anonymity import check_anonymity


def anonymity_level(file_name, quasi_ident, sens_att, l_new, new_file_name):
    """Function for check all the anonymity techniques under study."""
    k_anon = check_anonymity.calculate_k(file_name, quasi_ident)
    l_div = check_anonymity.calculate_l(file_name, quasi_ident, sens_att)
    entropy_l = check_anonymity.calculate_entropy_l(file_name, quasi_ident, sens_att)
    alpha, _ = check_anonymity.calculate_alpha_k(file_name, quasi_ident, sens_att)
    basic_beta = check_anonymity.calculate_basic_beta(file_name, quasi_ident, sens_att)
    enhanced_beta = check_anonymity.calculate_enhanced_beta(file_name, quasi_ident, sens_att)
    delta_disclosure = check_anonymity.calculate_delta_disclosure(file_name, quasi_ident, sens_att)
    t_clos = check_anonymity.calculate_t_closeness(file_name, quasi_ident, sens_att)
    c_div, _ = check_anonymity.calculate_c_l_diversity(file_name, quasi_ident, sens_att)

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

    data = check_anonymity.read_file(file_name)
    max_l = []
    for sa_value in sens_att:
        max_l.append(len(np.unique(data[sa_value].values)))
    max_l = min(max_l)

    assert l_new <= max_l, f'Error, the maximum value for l is {max_l}'
    df_new = check_anonymity.achieve_l_diversity(file_name, quasi_ident, sens_att, l_new)
    if len(df_new) > l_new:
        df_new.to_csv(new_file_name, index=False)
        print(f'Dataset veryfying l-diversity with l = {l_new} saved in: {new_file_name}.\n')
    else:
        print(f'The dataset cannot verify l-diversity with l = {l_new} only by suppression.\n')


QI = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']
SA = ['Drug']
FILE_NAME = './Data/Processed/drug_type.csv'
L_NEW = 2
NEW_FILE_NAME = f'./Data/l_diversity/drug_type_l{L_NEW}.csv'
anonymity_level(FILE_NAME, QI, SA, L_NEW, NEW_FILE_NAME)

L_NEW = 3
FILE_NAME = './Data/Processed/drugs_k5.csv'
NEW_FILE_NAME = f'./Data/l_diversity/drugs_k5_anonymized_l{L_NEW}.csv'
anonymity_level(FILE_NAME, QI, SA, L_NEW, NEW_FILE_NAME)

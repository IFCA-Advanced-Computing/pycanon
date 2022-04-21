"""Example using the airline passenger satisfaction dataset."""

import numpy as np
import test_anonymity_gen

def check_anonymity(file_name, quasi_ident, sens_att, l_new, new_file_name):
    """Function for check all the anonymity techniques under study."""
    k_anon = test_anonymity_gen.calculate_k(file_name, quasi_ident)
    l_div = test_anonymity_gen.calculate_l(file_name, quasi_ident, sens_att)
    entropy_l = test_anonymity_gen.calculate_entropy_l(file_name, quasi_ident, sens_att)
    alpha, _ = test_anonymity_gen.get_alpha_k(file_name, quasi_ident, sens_att)
    basic_beta = test_anonymity_gen.calculate_basic_beta(file_name, quasi_ident, sens_att)
    enhanced_beta = test_anonymity_gen.calculate_enhanced_beta(file_name, quasi_ident, sens_att)
    delta_disclosure = test_anonymity_gen.calculate_delta_disclosure(file_name, quasi_ident, sens_att)
    t_clos = test_anonymity_gen.calculate_t_closeness(file_name, quasi_ident, sens_att)
    c_div, _ = test_anonymity_gen.calculate_c_l_diversity(file_name, quasi_ident, sens_att)

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

    data = test_anonymity_gen.read_file(file_name)
    max_l = []
    for sa_value in sens_att:
        max_l.append(len(np.unique(data[sa_value].values)))
    max_l = min(max_l)

    assert l_new <= max_l, f'Error, the maximum value for l is {max_l}'
    df_new = test_anonymity_gen.l_diversity(file_name, quasi_ident, sens_att, l_new)
    if len(df_new) > l_new:
        df_new.to_csv(new_file_name, index = False)
        print(f'Dataset veryfying l-diversity with l = {l_new} saved in: {new_file_name}.\n')
    else:
        print(f'The dataset cannot verify l-diversity with l = {l_new} only by suppression.\n')

QI = ['Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class', 'Flight Distance',
    'Departure Delay in Minutes', 'Arrival Delay in Minutes']
SA = ['Departure/Arrival time convenient', 'Online boarding', 'On-board service',
    'Inflight service', 'Cleanliness', 'satisfaction']
L_NEW = 2
# FILE_NAME = './Data/Processed/airline_passenger_sat.csv' is not checked because of the
# large number of different values in Arrival Delay in Minutes and Departure Delay in Minutes
# NEW_FILE_NAME = f'./Data/l_diversity/airline_passenger_sat_l{L_NEW}.csv'
# check_anonymity(FILE_NAME, QI, SA, L_NEW, NEW_FILE_NAME)

for i in [2, 5, 10, 20]:
    FILE_NAME = f'./Data/Processed/airline_passenger_sat_k{i}.csv'
    NEW_FILE_NAME = f'./Data/l_diversity/airline_passenger_sat_k{i}_anonymized_l{L_NEW}.csv'
    check_anonymity(FILE_NAME, QI, SA, L_NEW, NEW_FILE_NAME)

"""Example using the airline passenger satisfaction dataset."""

import numpy as np
from src import test_anonymity

def check_anonymity(file_name, quasi_ident, sens_att):
    """Function for check all the anonymity techniques under study."""
    k_anon = test_anonymity.calculate_k(file_name, quasi_ident)
    l_div = test_anonymity.calculate_l(file_name, quasi_ident, sens_att)
    entropy_l = test_anonymity.calculate_entropy_l(file_name, quasi_ident, sens_att)
    alpha, _ = test_anonymity.calculate_alpha_k(file_name, quasi_ident, sens_att)
    basic_beta = test_anonymity.calculate_basic_beta(file_name, quasi_ident, sens_att)
    enhanced_beta = test_anonymity.calculate_enhanced_beta(file_name, quasi_ident, sens_att)
    delta_disclosure = test_anonymity.calculate_delta_disclosure(file_name, quasi_ident, sens_att)
    t_clos = test_anonymity.calculate_t_closeness(file_name, quasi_ident, sens_att)
    c_div, _ = test_anonymity.calculate_c_l_diversity(file_name, quasi_ident, sens_att)

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

QI = ['Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class', 'Flight Distance',
    'Departure Delay in Minutes', 'Arrival Delay in Minutes']
SA = ['Departure/Arrival time convenient', 'Online boarding', 'On-board service',
    'Inflight service', 'Cleanliness', 'satisfaction']
# FILE_NAME = './Data/Processed/airline_passenger_sat.csv' is not checked because of the
# large number of different values in Arrival Delay in Minutes and Departure Delay in Minutes
for i in [2, 5, 10, 20]:
    FILE_NAME = f'./Data/Processed/airline_passenger_sat_k{i}.csv'
    check_anonymity(FILE_NAME, QI, SA)

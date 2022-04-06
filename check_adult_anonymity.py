import numpy as np
import pandas as pd
import test_anonymity


def check_anonymity(file, QI, SA, l_new, new_file_name):
    df = pd.read_csv(file)

    max_l = []
    for sa in SA:
        max_l.append(len(np.unique(df[sa].values)))
    max_l = min(max_l)

    k = test_anonymity.calculate_k(df, QI)
    l = test_anonymity.calculate_l(df, QI, SA)
    entropy_l = test_anonymity.calculate_entropy_l(df, QI, SA)
    alpha, k_alpha = test_anonymity.get_alpha_k(df, QI, SA)

    assert k == k_alpha, 'Error. Check get_alpha_k() and calculate_k()'
    print(f'File: {file}. The dataset verifies k-anonimity with k={k}, l-diversity with l={l}, ')
    print(f'entropy l-diversity with l={entropy_l} and (alpha,k)-anonymity with alpha={alpha} and k={k}')

    assert l_new <= max_l, f'Error, the maximum value for l is {max_l}' 
    df_new = test_anonymity.l_diversity(df, QI, SA, l_new)
    assert test_anonymity.calculate_l(df_new, QI, SA) == l_new, 'Error, check l_diversity()'

    df_new.to_csv(new_file_name, index = False)
    print(f'Dataset veryfying l-diversity with l={l_new} saved in: {new_file_name} \n')
    
QI = ['age', 'education', 'occupation', 'relationship', 'sex', 'native-country']
SA = ['salary-class']
file = './Data/adult_anonymized_3.csv'
l_new = 2
new_file_name = './Data/adult_anonymized_3_l' + str(l_new) + '.csv'
check_anonymity(file, QI, SA, l_new, new_file_name)

file = './Data/adult_anonymized_10.csv'
new_file_name = './Data/adult_anonymized_10_l' + str(l_new) + '.csv'
check_anonymity(file, QI, SA, l_new, new_file_name)

file = './Data/adult_anonymized_20.csv'
new_file_name = './Data/adult_anonymized_20_l' + str(l_new) + '.csv'
check_anonymity(file, QI, SA, l_new, new_file_name)
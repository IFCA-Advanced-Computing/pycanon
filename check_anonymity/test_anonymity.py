"""Module with different functions which calculate properties about anonymity:
k.anonimity, (alpha,k)-anonymity, l-diversity, entropy l-diversity, (c,l)-diversity,
basic beta-likeness, enhanced beta-likeness, t-closeness and delta-disclosure privacy."""

import os
import numpy as np
import pandas as pd

def read_file(file_name):
    """Read the given file.

    Parameter file_name: name of the file with the data under study.
    Precondition: file_name must have csv, xlsx, sav or txt extension.
    """
    _, file_extension = os.path.splitext(file_name)
    if file_extension in ['.csv', '.xlsx', '.sav', '.txt']:
        if file_extension in ['.csv', '.txt']:
            data = pd.read_csv(file_name)
        elif file_extension == '.xlsx':
            data = pd.read_excel(file_name)
        else:
            data = pd.read_spss(file_name)
    else:
        raise ValueError('Invalid file extension.')
    return data

def check_qi(data, quasi_ident):
    """"Checks if the entered quasi-identifiers are valid.

    Parameter data: dataframe with the data under study.
    Precondition: data is a pandas dataframe.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.
    """
    cols = data.columns
    err_val = [i for i, v in enumerate([qi in cols for qi in quasi_ident]) if v is False]
    if len(err_val) > 0:
        raise ValueError(f'''Values not defined: {[quasi_ident[i] for i in err_val]}.
                          Cannot be quasi-identifiers''')

def check_sa(data, sens_att):
    """"Checks if the entered sensitive attributes are valid.

    Parameter data: dataframe with the data under study.
    Precondition: data is a pandas dataframe.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    cols = data.columns
    err_val = [i for i, v in enumerate([sa in cols for sa in sens_att]) if v is False]
    if len(err_val) > 0:
        raise ValueError(f'''Values not defined: {[sens_att[i] for i in err_val]}.
                          Cannot be sensitive attributes''')

def intersect(tmp):
    """Intersect two sets: the first and the second of the given list.

    Parameter tmp: list of numpy arrays.
    Precondition: tmp is a list of sets sorted in decreasing order of cardinality.
    """
    i, j = 0, 0
    tmp_new = []
    while i < len(tmp[0]):
        tmp1 = tmp[0][i]
        tmp2 = tmp[1][j]
        tmp_new.append(np.intersect1d(tmp1, tmp2))
        if j < len(tmp[1])-1:
            j += 1
        else:
            j = 0
            i +=1
    tmp[1] = tmp_new
    tmp = tmp[1:]
    return tmp

def get_equiv_class(data, quasi_ident):
    """"Find the equivalence classes present in the dataset.

    Parameter data: dataframe with the data under study.
    Precondition: data is a pandas dataframe.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.
    """
    index = []
    for qi in quasi_ident:
        values = np.unique(data[qi].values)
        tmp = [np.unique(data[data[qi] == value].index) for value in values]
        index.append(tmp)
    index = sorted(index, key = lambda x: len(x))
    equiv_class = index.copy()
    while len(equiv_class) > 1:
        equiv_class = intersect(equiv_class)
        equiv_class = sorted(equiv_class, key = lambda x: len(x))
    equiv_class = [x for x in equiv_class[0] if len(x) > 0]
    return equiv_class

def calculate_k(file_name, quasi_ident):
    """Calculate k for k-anonymity.

    Parameter file_name: name of the file with the data under study.
    Precondition: file_name must have csv, xlsx, sav or txt extension.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.
    """
    data = read_file(file_name)
    check_qi(data, quasi_ident)
    equiv_class = get_equiv_class(data, quasi_ident)
    k_anon = min([len(x) for x in equiv_class])
    return k_anon

def aux_calculate_k(data, quasi_ident):
    """Calculate k for k-anonymity.

    Parameter data: dataframe with the data under study.
    Precondition: data is a pandas dataframe.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.
    """
    check_qi(data, quasi_ident)
    equiv_class = get_equiv_class(data, quasi_ident)
    k_anon = min([len(x) for x in equiv_class])
    return k_anon

def convert(set_):
    """Converts a set to a list.

    Parameter set_: set which will be aconvert into a list.
    Precondition: set_ is a set.
    """
    return [*set_, ]

def calculate_l(file_name, quasi_ident, sens_att, gen = True):
    """Calculate l for l-diversity.

    Parameter file_name: name of the file with the data under study.
    Precondition: file_name must have csv, xlsx, sav or txt extension.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    quasi_ident = np.array(quasi_ident)
    sens_att = np.array(sens_att)
    data = read_file(file_name)
    check_qi(data, quasi_ident)
    check_sa(data, sens_att)
    equiv_class = get_equiv_class(data, quasi_ident)
    l_div = []
    if gen:
        for ec in equiv_class:
            data_temp = data.iloc[convert(ec)]
            l_sa = [len(np.unique(data_temp[sa].values)) for sa in sens_att]
            l_div.append(min(l_sa))
    else:
        for i, sa in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            equiv_class = get_equiv_class(data, tmp_qi)
            l_ec = []
            for ec in equiv_class:
                data_temp = data.iloc[convert(ec)]
                l_ec.append(len(np.unique(data_temp[sa].values)))
            l_div.append(min(l_ec))
    return min(l_div)

def l_diversity(file_name, quasi_ident, sens_att, l_new):
    """Given l, transform the dataset into a new one checking l-diversity for the new l, only
    using suppression.

    Parameter file_name: name of the file with the data under study.
    Precondition: file_name must have csv, xlsx, sav or txt extension.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.

    Parameter l_new: l value for l-diversity.
    Precondition: l_new is an int.
    """
    data = read_file(file_name)
    check_qi(data, quasi_ident)
    check_sa(data, sens_att)
    equiv_class = get_equiv_class(data, quasi_ident)
    l_ec = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        l_sa = [len(np.unique(data_temp[sa].values)) for sa in sens_att]
        l_ec.append(min(l_sa))
    data_ec_l = pd.DataFrame({'equiv_class': equiv_class, 'l_ec': l_ec})
    data_ec_l = data_ec_l[data_ec_l.l_ec < l_new]
    ec_elim = np.concatenate([convert(x) for x in data_ec_l.equiv_class.values])
    data_new = data.drop(ec_elim).reset_index()
    data_new.drop('index', inplace=True, axis=1)
    return data_new


def calculate_entropy_l(file_name, quasi_ident, sens_att, gen = True):
    """Calculate l for entropy l-diversity.

    Parameter file_name: name of the file with the data under study.
    Precondition: file_name must have csv, xlsx, sav or txt extension.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    quasi_ident = np.array(quasi_ident)
    data = read_file(file_name)
    check_qi(data, quasi_ident)
    check_sa(data, sens_att)
    if gen:
        equiv_class = get_equiv_class(data, quasi_ident)
        entropy_ec = []
        for ec in equiv_class:
            data_temp = data.iloc[convert(ec)]
            entropy_sa = []
            for sa in sens_att:
                values = np.unique(data_temp[sa].values)
                p = [len(data_temp[data_temp[sa] == s])/len(data_temp) for s in values]
                entropy = np.sum(p*np.log(p))
                entropy_sa.append(-entropy)
            entropy_ec.append(min(entropy_sa))
        ent_l = int(min(np.exp(1)**entropy_ec))
    else:
        entropy_sa = []
        for i, sa in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            equiv_class = get_equiv_class(data, tmp_qi)
            entropy_ec = []
            for ec in equiv_class:
                data_temp = data.iloc[convert(ec)]
                entropy = 0
                for s in np.unique(data_temp[sa].values):
                    p = len(data_temp[data_temp[sa] == s])/len(data_temp)
                    entropy += p*np.log(p)
                entropy_ec.append(-entropy)
            entropy_sa.append(min(entropy_ec))
        ent_l = int(min(np.exp(1)**entropy_sa))
    return ent_l

def calculate_c_l_diversity(file_name, quasi_ident, sens_att, imp = 0, gen = True):
    """Calculate c and l for recursive (c,l)-diversity.

    Parameter file_name: name of the file with the data under study.
    Precondition: file_name must have csv, xlsx, sav or txt extension.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.

    Parameter imp: impression level.
    Precondition: imp is an int, imp = 1 if comments need to be displayed.
    """
    quasi_ident = np.array(quasi_ident)
    data = read_file(file_name)
    check_qi(data, quasi_ident)
    check_sa(data, sens_att)
    l_div = calculate_l(file_name, quasi_ident, sens_att)
    if l_div > 1:
        c_div = []
        if gen:
            equiv_class = get_equiv_class(data, quasi_ident)
            for sens_att_value in sens_att:
                c_sa = []
                for ec in equiv_class:
                    data_temp = data.iloc[convert(ec)]
                    values = np.unique(data_temp[sens_att_value].values)
                    r_ec = np.sort([len(data_temp[data_temp[sens_att_value] == s]) for s in values])
                    c_sa.append(np.floor(r_ec[0]/sum(r_ec[l_div - 1:]) + 1))
                c_div.append(int(max(c_sa)))
            c_div = max(c_div)
        else:
            for i, sa in enumerate(sens_att):
                tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
                equiv_class = get_equiv_class(data, tmp_qi)
                c_sa = []
                for ec in equiv_class:
                    data_temp = data.iloc[convert(ec)]
                    values = np.unique(data_temp[sa].values)
                    r_ec = np.sort([len(data_temp[data_temp[sa] == s]) for s in values])
                    c_sa.append(np.floor(r_ec[0]/sum(r_ec[l_div - 1:]) + 1))
                c_div.append(int(max(c_sa)))
            c_div = max(c_div)
    else:
        if imp == 1:
            print(f'c for (c,l)-diversity cannot be calculated as l={l_div}')
        c_div = np.nan
    return c_div, l_div


def get_alpha_k(file_name, quasi_ident, sens_att, gen = True):
    """Calculate alpha and k for (alpha,k)-anonymity.

    Parameter file_name: name of the file with the data under study.
    Precondition: file_name must have csv, xlsx, sav or txt extension.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    quasi_ident = np.array(quasi_ident)
    data = read_file(file_name)
    k_anon = calculate_k(file_name, quasi_ident)
    equiv_class = get_equiv_class(data, quasi_ident)
    if gen:
        alpha_ec = []
        for ec in equiv_class:
            data_temp = data.iloc[convert(ec)]
            alpha_sa = []
            for sa in sens_att:
                values = np.unique(data_temp[sa].values)
                _alpha = [len(data_temp[data_temp[sa] == s])/len(data_temp) for s in values]
                alpha_sa.append(max(_alpha))
            alpha_ec.append(max(alpha_sa))
        alpha = max(alpha_ec)
    else:
        alpha_sa = []
        for i, sa in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            equiv_class = get_equiv_class(data, tmp_qi)
            alpha_ec = []
            for ec in equiv_class:
                data_temp = data.iloc[convert(ec)]
                values = np.unique(data_temp[sa].values)
                _alpha = [len(data_temp[data_temp[sa] == s])/len(data_temp) for s in values]
                alpha_ec.append(max(_alpha))
            alpha_sa.append(max(alpha_ec))
        alpha = max(alpha_sa)
    return alpha, k_anon


def aux_calculate_beta(data, quasi_ident, sens_att_value):
    """Auxiliary function for beta calculation for basic and enhanced beta-likeness.

    Parameter data: dataframe with the data under study.
    Precondition: data is a pandas dataframe.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    p = np.array([len(data[data[sens_att_value] == s])/len(data) for s in values])
    q = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        qi = np.array([len(data_temp[data_temp[sens_att_value] == s])/len(ec) for s in values])
        q.append(qi)
    dist = [max((q[i]-p)/p) for i in range(len(equiv_class))]
    return p, dist

def calculate_basic_beta(file_name, quasi_ident, sens_att, gen = True):
    """Calculate beta for basic beta-likeness.

    Parameter file_name: name of the file with the data under study.
    Precondition: file_name must have csv, xlsx, sav or txt extension.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    quasi_ident = np.array(quasi_ident)
    data = read_file(file_name)
    check_qi(data, quasi_ident)
    check_sa(data, sens_att)
    beta_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            _, dist = aux_calculate_beta(data, quasi_ident, sens_att_value)
            beta_sens_att.append(max(dist))
    else:
        for i, sens_att_value in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            _, dist = aux_calculate_beta(data, tmp_qi, sens_att_value)
            beta_sens_att.append(max(dist))
    beta = max(beta_sens_att)
    return beta

def calculate_enhanced_beta(file_name, quasi_ident, sens_att, gen = True):
    """Calculate beta for enhanced beta-likeness.

    Parameter file_name: name of the file with the data under study.
    Precondition: file_name must have csv, xlsx, sav or txt extension.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    quasi_ident = np.array(quasi_ident)
    data = read_file(file_name)
    check_qi(data, quasi_ident)
    check_sa(data, sens_att)
    beta_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            p, dist = aux_calculate_beta(data, quasi_ident, sens_att_value)
            min_beta_lnp = [min(max(dist), -np.log(p_i)) for p_i in p]
            beta_sens_att.append(max(min_beta_lnp))
    else:
        for i, sens_att_value in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            p, dist = aux_calculate_beta(data, tmp_qi, sens_att_value)
            min_beta_lnp = [min(max(dist), -np.log(p_i)) for p_i in p]
            beta_sens_att.append(max(min_beta_lnp))
    beta = max(beta_sens_att)
    return beta

def aux_calculate_delta_disclosure(data, quasi_ident, sens_att_value):
    """Auxiliary function for delta calculation for delta-disclousure privacy.

    Parameter data: dataframe with the data under study.
    Precondition: data is a pandas dataframe.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    p = np.array([len(data[data[sens_att_value] == s])/len(data) for s in values])
    q = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        qi = np.array([len(data_temp[data_temp[sens_att_value] == s])/len(ec) for s in values])
        q.append(qi)
    aux = [max([np.abs(np.log(x)) for x in qi/p if x > 0]) for qi in q]
    return aux

def calculate_delta_disclosure(file_name, quasi_ident, sens_att, gen = True):
    """Calculate delta for delta-disclousure privacy.

    Parameter file_name: name of the file with the data under study.
    Precondition: file_name must have csv, xlsx, sav or txt extension.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    quasi_ident = np.array(quasi_ident)
    data = read_file(file_name)
    check_qi(data, quasi_ident)
    check_sa(data, sens_att)
    delta_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            aux = aux_calculate_delta_disclosure(data, quasi_ident, sens_att_value)
            delta_sens_att.append(max(aux))
    else:
        for i, sens_att_value in enumerate(sens_att):
            tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
            aux = aux_calculate_delta_disclosure(data, tmp_qi, sens_att_value)
            delta_sens_att.append(max(aux))
    delta = max(delta_sens_att)
    return delta

def aux_t_closeness_num(data, quasi_ident, sens_att_value):
    """Auxiliary function for t calculation for t-closeness. Function used for numerical
    attributes: the definition of the EMD is used.

    Parameter data: dataframe with the data under study.
    Precondition: data is a pandas dataframe.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    m = len(values)
    p = np.array([len(data[data[sens_att_value] == s])/len(data) for s in values])
    emd = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        qi = np.array([len(data_temp[data_temp[sens_att_value] == s])/len(ec) for s in values])
        r =  qi - p
        abs_r, emd_ec = 0, 0
        for i in range(m):
            abs_r += r[i]
            emd_ec += np.abs(abs_r)
        emd_ec = 1/(m-1) * emd_ec
        emd.append(emd_ec)
    return max(emd)

def aux_t_closeness_str(data, quasi_ident, sens_att_value):
    """Auxiliary function for t calculation for t-closeness. Function used for categorical
    attributes: the metric "Equal Distance" is used.

    Parameter data: dataframe with the data under study.
    Precondition: data is a pandas dataframe.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    m = len(values)
    p = np.array([len(data[data[sens_att_value] == s])/len(data) for s in values])
    emd = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        qi = np.array([len(data_temp[data_temp[sens_att_value] == s])/len(ec) for s in values])
        r =  qi - p
        emd_ec = 0
        for i in range(m):
            emd_ec += np.abs(r[i])
        emd_ec = 0.5 * emd_ec
        emd.append(emd_ec)
    return max(emd)

def calculate_t_closeness(file_name, quasi_ident, sens_att, gen = True):
    """Calculate t for t-closeness.

    Parameter file_name: name of the file with the data under study.
    Precondition: file_name must have csv, xlsx, sav or txt extension.

    Parameter quasi_ident: list with the name of the columns of the dataframe
    that are quasi-identifiers.
    Precondition: quasi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    quasi_ident = np.array(quasi_ident)
    data = read_file(file_name)
    check_qi(data, quasi_ident)
    check_sa(data, sens_att)
    t_sens_att = []
    if gen:
        for sens_att_value in sens_att:
            if pd.api.types.is_numeric_dtype(data[sens_att_value]):
                t_sens_att.append(aux_t_closeness_num(data, quasi_ident, sens_att_value))
            elif pd.api.types.is_string_dtype(data[sens_att_value]):
                t_sens_att.append(aux_t_closeness_str(data, quasi_ident, sens_att_value))
            else:
                raise ValueError('Error, invalid sens_att value type')
    else:
        for i, sens_att_value in enumerate(sens_att):
            if pd.api.types.is_numeric_dtype(data[sens_att_value]):
                tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
                t_sens_att.append(aux_t_closeness_num(data, tmp_qi, sens_att_value))
            elif pd.api.types.is_string_dtype(data[sens_att_value]):
                tmp_qi = np.concatenate([quasi_ident, np.delete(sens_att, i)])
                t_sens_att.append(aux_t_closeness_str(data, tmp_qi, sens_att_value))
            else:
                raise ValueError('Error, invalid sens_att value type')
    return max(t_sens_att)

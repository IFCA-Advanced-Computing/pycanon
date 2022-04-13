"""Module with different functions which calculate properties about anonymity:
k.anonimity, (alpha,k)-anonymity, l-diversity, entropy l-diversity, (c,l)-diversity,
basic beta-likeness, enhanced beta-likeness, t-closeness and delta-disclosure privacy."""

import numpy as np
import pandas as pd

def intersect(tmp):
    """Intersect two sets: the first and the second of the given list.

    Parameter tmp: list of sets.
    Precondition: tmp is a list of sets sorted in decreasing order of cardinality.
    """
    i, j = 0, 0
    tmp_new = []
    while i < len(tmp[0]):
        tmp1 = tmp[0][i]
        tmp2 = tmp[1][j]
        tmp_new.append(tmp1.intersection(tmp2))
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
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.
    """
    index = []
    for qi in quasi_ident:
        values = np.unique(data[qi].values)
        tmp = []
        for value in values:
            tmp.append(set(data[data[qi] == value].index))
        index.append(tmp)
    index = sorted(index, key = lambda x: len(x))
    equiv_class = index.copy()
    while len(equiv_class) > 1:
        equiv_class = intersect(equiv_class)
        equiv_class = sorted(equiv_class, key = lambda x: len(x))
    equiv_class = [x for x in equiv_class[0] if len(x) > 0]
    return equiv_class

def calculate_k(data, quasi_ident):
    """Calculate k for k-anonymity.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    k_anon = min([len(x) for x in equiv_class])
    return k_anon

def convert(set_):
    """Converts a set to a list.

    Parameter set_: set which will be aconvert into a list.
    Precondition: set_ is a set.
    """
    return [*set_, ]

def calculate_l(data, quasi_ident, sens_att):
    """Calculate l for l-diversity.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    l_div = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        l_sa = []
        for sa in sens_att:
            l_sa.append(len(np.unique(data_temp[sa].values)))
        l_div.append(min(l_sa))
    return min(l_div)

def l_diversity(data, quasi_ident, sens_att, l_new):
    """Given l, transform the dataset into a new one checking l-diversity for the new l, only
    using suppression.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.

    Parameter l_new: l value for l-diversity.
    Precondition: l_new is an int.
    """

    equiv_class = get_equiv_class(data, quasi_ident)
    l_ec = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        l_sa = []
        for sa in sens_att:
            l_sa.append(len(np.unique(data_temp[sa].values)))
        l_ec.append(min(l_sa))
    data_ec_l = pd.DataFrame({'equiv_class': equiv_class, 'l_ec': l_ec})
    data_ec_l = data_ec_l[data_ec_l.l_ec < l_new]
    ec_elim = np.concatenate([convert(x) for x in data_ec_l.equiv_class.values])
    data_new = data.drop(ec_elim).reset_index()
    data_new.drop('index', inplace=True, axis=1)
    return data_new

def calculate_entropy_l(data, quasi_ident, sens_att):
    """Calculate l for entropy l-diversity.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    entropy_ec = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        entropy_sa = []
        for sa in sens_att:
            entropy = 0
            for s in np.unique(data_temp[sa].values):
                p = len(data_temp[data_temp[sa] == s])/len(data_temp)
                entropy += p*np.log(p)
            entropy_sa.append(-entropy)
        entropy_ec.append(max(entropy_sa))
    ent_l = int(min(np.exp(1)**entropy_ec))
    return ent_l

def calculate_c_l_diversity(data, quasi_ident, sens_att, imp = 0):
    """Calculate c and l for recursive (c,l)-diversity.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.

    Parameter imp: impression level.
    Precondition: imp is an int, imp = 1 if comments need to be displayed.
    """
    l_div = calculate_l(data, quasi_ident, sens_att)
    equiv_class = get_equiv_class(data, quasi_ident)
    if l_div > 1:
        c_div = []
        for sens_att_value in sens_att:
            c_sa = []
            for ec in equiv_class:
                data_temp = data.iloc[convert(ec)]
                r_ec = []
                for s in np.unique(data_temp[sens_att_value].values):
                    r_ec.append(len(data_temp[data_temp[sens_att_value] == s]))
                r_ec = np.sort(r_ec)
                c_sa.append(np.floor(r_ec[0]/sum(r_ec[l_div - 1:]) + 1))
            c_div.append(int(max(c_sa)))
        c_div = max(c_div)
    else:
        if imp == 1:
            print(f'c for (c,l)-diversity cannot be calculated as l={l_div}')
        c_div = np.nan
    return c_div, l_div


def get_alpha_k(data, quasi_ident, sens_att):
    """Calculate alpha and k for (alpha,k)-anonymity.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    k_anon = calculate_k(data, quasi_ident)
    equiv_class = get_equiv_class(data, quasi_ident)
    alpha_ec = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        alpha_sa = []
        for sa in sens_att:
            alpha = []
            for s in np.unique(data_temp[sa].values):
                alpha.append(len(data_temp[data_temp[sa] == s])/len(data_temp))
            alpha_sa.append(max(alpha))
        alpha_ec.append(max(alpha_sa))
    return max(alpha_ec), k_anon

def aux_calculate_beta(data, quasi_ident, sens_att_value):
    """Auxiliary function for beta calculation for basic and enhanced beta-likeness.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    n = len(data)
    p = []
    for s in values:
        p.append(len(data[data[sens_att_value] == s])/n)
    q = []
    for i in range(len(equiv_class)):
        qi = []
        n_ec = len(equiv_class[i])
        data_temp = data.iloc[convert(equiv_class[i])]
        for s in values:
            qi.append(len(data_temp[data_temp[sens_att_value] == s])/n_ec)
        q.append(np.array(qi))
    dist = []
    for i in range(len(equiv_class)):
        dist.append(max((q[i]-p)/p))
    return p, dist

def calculate_basic_beta(data, quasi_ident, sens_att):
    """Calculate beta for basic beta-likeness.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    beta_sens_att = []
    for sens_att_value in sens_att:
        _, dist = aux_calculate_beta(data, quasi_ident, sens_att_value)
        beta_sens_att.append(max(dist))
    beta = max(beta_sens_att)
    return beta

def calculate_enhanced_beta(data, quasi_ident, sens_att):
    """Calculate beta for enhanced beta-likeness.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    beta_sens_att = []
    for sens_att_value in sens_att:
        p, dist = aux_calculate_beta(data, quasi_ident, sens_att_value)
        min_beta_lnp = []
        for p_i in p:
            min_beta_lnp.append(min(max(dist), -np.log(p_i)))
        beta_sens_att.append(max(min_beta_lnp))
    beta = max(beta_sens_att)
    return beta

def aux_calculate_delta_disclosure(data, quasi_ident, sens_att_value):
    """Auxiliary function for delta calculation for delta-disclousure privacy.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    n = len(data)
    p = []
    for s in values:
        p.append(len(data[data[sens_att_value] == s])/n)
    q = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        qi = []
        n_ec = len(ec)
        for s in values:
            qi.append(len(data_temp[data_temp[sens_att_value] == s])/n_ec)
        q.append(np.array(qi))
    aux = []
    for i in range(len(q)):
        aux.append(max([np.abs(np.log(x)) for x in q[i]/p if x>0]))
    return aux

def calculate_delta_disclosure(data, quasi_ident, sens_att):
    """Calculate delta for delta-disclousure privacy.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    delta_sens_att = []
    for sens_att_value in sens_att:
        aux = aux_calculate_delta_disclosure(data, quasi_ident, sens_att_value)
        delta_sens_att.append(max(aux))
    delta = max(delta_sens_att)
    return delta

def aux_t_closeness_num(data, quasi_ident, sens_att_value):
    """Auxiliary function for t calculation for t-closeness. Function used for numerical
    attributes: the definition of the EMD is used.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    m = len(values)
    n = len(data)
    p = []
    for s in values:
        p.append(len(data[data[sens_att_value] == s])/n)
    emd = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        qi = []
        n_ec = len(ec)
        for s in values:
            qi.append(len(data_temp[data_temp[sens_att_value] == s])/n_ec)
        emd_ec = 0
        r =  np.array(p) - np.array(qi)
        abs_r = 0
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
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    equiv_class = get_equiv_class(data, quasi_ident)
    values = np.unique(data[sens_att_value].values)
    m = len(values)
    n = len(data)
    p = []
    for s in values:
        p.append(len(data[data[sens_att_value] == s])/n)
    emd = []
    for ec in equiv_class:
        data_temp = data.iloc[convert(ec)]
        qi = []
        n_ec = len(ec)
        for s in values:
            qi.append(len(data_temp[data_temp[sens_att_value] == s])/n_ec)
        r =  np.array(p) - np.array(qi)
        emd_ec = 0
        for i in range(m):
            emd_ec += np.abs(r[i])
        emd_ec = 0.5 * emd_ec
        emd.append(emd_ec)
    return max(emd)

def calculate_t_closeness(data, quasi_ident, sens_att):
    """Calculate t for t-closeness.

    Parameter data: dataframe with the data under study.
    Predondition: data is a pandas dataframe.

    Parameter quisi_ident: list with the name of the columns of the dataframe
    that are quiasi-identifiers.
    Precondition: quisi_ident is a list of strings.

    Parameter sens_att: list with the name of the columns of the dataframe
    that are the sensitive attributes.
    Precondition: sens_att is a list of strings.
    """
    t_sens_att = []
    for sens_att_value in sens_att:
        if pd.api.types.is_numeric_dtype(data[sens_att[0]]):
            t_sens_att.append(aux_t_closeness_num(data, quasi_ident, sens_att_value))
        elif pd.api.types.is_string_dtype(data[sens_att[0]]):
            t_sens_att.append(aux_t_closeness_str(data, quasi_ident, sens_att_value))
        else:
            raise ValueError('Error, invalid sens_att value type')
    return max(t_sens_att)

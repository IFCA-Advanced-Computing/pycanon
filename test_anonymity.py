import numpy as np
import pandas as pd

def itersec(tmp):
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

def get_equiv_class(df, QI):
    index = []
    for qi in QI:
        values = np.unique(df[qi].values)
        tmp = []
        for value in values:
            tmp.append(set(df[df[qi] == value].index))
        index.append(tmp)
    
    index = sorted(index, key = lambda x: len(x))
    equiv_class = index.copy()
    while len(equiv_class) > 1:
        equiv_class = itersec(equiv_class)
        equiv_class = sorted(equiv_class, key = lambda x: len(x))
    equiv_class = equiv_class[0]
    equiv_class = [x for x in equiv_class if len(x) > 0]
    return equiv_class

def calculate_k(df, QI):
    equiv_class = get_equiv_class(df, QI)
    k = min([len(x) for x in equiv_class])
    return k

def convert(set):
    return [*set, ]

def calculate_l(df, QI, SA):
    equiv_class = get_equiv_class(df, QI)
    l = []
    for i in range(len(equiv_class)):
        df_temp = df.iloc[convert(equiv_class[i])]  
        l_sa = []
        for sa in SA: 
            l_sa.append(len(np.unique(df_temp[sa].values)))
        l.append(min(l_sa))
    l = min(l) 
    return l


def l_diversity(df, QI, SA, l_new):
    equiv_class = get_equiv_class(df, QI)
    l = []
    for i in range(len(equiv_class)):
        df_temp = df.iloc[convert(equiv_class[i])]  
        l_sa = []
        for sa in SA: 
            l_sa.append(len(np.unique(df_temp[sa].values)))
        l.append(min(l_sa))
        
    df_EC_l = pd.DataFrame({'equiv_class': equiv_class, 'l': l})
    df_EC_l = df_EC_l[df_EC_l.l < l_new]
    ec_elim = np.concatenate([convert(x) for x in df_EC_l.equiv_class.values])
    df_new = df.drop(ec_elim).reset_index()
    df_new.drop('index', inplace=True, axis=1)
    return df_new

def calculate_entropy_l(df, QI, SA):
    equiv_class = get_equiv_class(df, QI)
    entropy_EC = []
    for i in range(len(equiv_class)):
        df_temp = df.iloc[convert(equiv_class[i])]  
        entropy_sa = []
        for sa in SA: 
            entropy = 0
            for s in np.unique(df_temp[sa].values):
                p = len(df_temp[df_temp[sa] == s])/len(df_temp)
                entropy += p*np.log(p)
            entropy_sa.append(-entropy) 
        entropy_EC.append(max(entropy_sa)) #Revisar
    l = int(min(np.exp(1)**entropy_EC) - 1)
    return l

def get_alpha_k(df, QI, SA):
    k = calculate_k(df, QI)
    equiv_class = get_equiv_class(df, QI)
    alpha_EC = []
    for i in range(len(equiv_class)):
        df_temp = df.iloc[convert(equiv_class[i])] 
        alpha_sa = []
        for sa in SA: 
            alpha = []
            for s in np.unique(df_temp[sa].values):
                alpha.append(len(df_temp[df_temp[sa] == s])/len(df_temp))
            alpha_sa.append(max(alpha))
        alpha_EC.append(max(alpha_sa))
    return max(alpha_EC), k

def aux_calculate_beta(df, QI, SA_value):
    equiv_class = get_equiv_class(df, QI)
    values = np.unique(df[SA_value].values)
    n = len(df)
    p = []
    for s in values:
        p.append(len(df[df[SA_value] == s])/n)
    
    q = []    
    for i in range(len(equiv_class)):
        qi = []
        n_ec = len(equiv_class[i])
        df_temp = df.iloc[convert(equiv_class[i])]  
        for s in values:
            qi.append(len(df_temp[df_temp[SA_value] == s])/n_ec)
        q.append(np.array(qi))
    
    dist = []
    for i in range(len(equiv_class)):
        dist.append(max((q[i]-p)/p))
    return p, dist

def calculate_basic_beta(df, QI, SA):
    beta_SA = []
    for SA_value in SA:
        _, dist = aux_calculate_beta(df, QI, SA_value) 
        beta_SA.append(max(dist))
    beta = max(beta_SA)
    return beta

def calculate_enhanced_beta(df, QI, SA):
    beta_SA = []
    for SA_value in SA:
        p, dist = aux_calculate_beta(df, QI, SA_value) 
        min_beta_lnp = []
        for i in range(len(p)):
            min_beta_lnp.append(min(dist[i], -np.log(p[i])))
        beta_SA.append(max(min_beta_lnp))
    beta = max(beta_SA)
    return beta

def aux_calculate_delta_disclosure(df, QI, SA_value):
    equiv_class = get_equiv_class(df, QI)
    values = np.unique(df[SA_value].values)
    n = len(df)
    p = []
    for s in values:
        p.append(len(df[df[SA_value] == s])/n)

    q = []    
    for i in range(len(equiv_class)):
        qi = []
        n_ec = len(equiv_class[i])
        df_temp = df.iloc[convert(equiv_class[i])]  
        for s in values:
            qi.append(len(df_temp[df_temp[SA_value] == s])/n_ec)
        q.append(np.array(qi))

    aux = []
    for i in range(len(q)):
        aux.append(max([np.abs(np.log(x)) for x in q[i]/p if x>0]))

    return aux

def calculate_delta_disclosure(df, QI, SA):
    delta_SA = []
    for SA_value in SA:
        aux = aux_calculate_delta_disclosure(df, QI, SA_value) 
        delta_SA.append(max(aux))
    delta = max(delta_SA)
    return delta

def aux_t_closeness_num(df, QI, SA_value):
    equiv_class = get_equiv_class(df, QI)
    values = np.unique(df[SA_value].values)
    m = len(values)
    n = len(df)
    p = []
    for s in values:
        p.append(len(df[df[SA_value] == s])/n)
    
    emd = []
    for i in range(len(equiv_class)):
        qi = []
        n_ec = len(equiv_class[i])
        df_temp = df.iloc[convert(equiv_class[i])]  
        for s in values:
            qi.append(len(df_temp[df_temp[SA_value] == s])/n_ec)
            
        emd_ec = 0
        r =  np.array(p) - np.array(qi)
        abs_r = 0
        for i in range(m):
            abs_r += r[i]
            emd_ec += np.abs(abs_r)
        emd_ec = 1/(m-1) * emd_ec
        emd.append(emd_ec)
    
    t = max(emd)
    return t
            
def aux_t_closeness_str(df, QI, SA_value):
    equiv_class = get_equiv_class(df, QI)
    values = np.unique(df[SA_value].values)
    m = len(values)
    n = len(df)
    p = []
    for s in values:
        p.append(len(df[df[SA_value] == s])/n)
        
    emd = []
    for i in range(len(equiv_class)):
        qi = []
        n_ec = len(equiv_class[i])
        df_temp = df.iloc[convert(equiv_class[i])]  
        for s in values:
            qi.append(len(df_temp[df_temp[SA_value] == s])/n_ec)
            
        r =  np.array(p) - np.array(qi)
        emd_ec = 0
        for i in range(m):
            emd_ec += np.abs(r[i])
        emd_ec = 0.5 * emd_ec
        emd.append(emd_ec)
        
    t = max(emd)
    return t
        
        
def calculate_t_closeness(df, QI, SA):
    t_SA = []
    for SA_value in SA:
        if pd.api.types.is_numeric_dtype(df[SA[0]]):
            t = aux_t_closeness_num(df, QI, SA_value)
        elif pd.api.types.is_string_dtype(df[SA[0]]):
            t = aux_t_closeness_str(df, QI, SA_value)
        else:
            raise ValueError('Error, invalid SA value type')
        t_SA.append(t)
        
    t = max(t_SA)
    return t
            
import numpy as np
import pandas as pd

file = 'StudentsMath_Score.sav'
new_file = 'StudentsMath_Score.csv'

def sav_to_csv(file, new_file):
    df = pd.read_spss(file)
    df.to_csv(new_file, index = False)
    
sav_to_csv(file, new_file)
    

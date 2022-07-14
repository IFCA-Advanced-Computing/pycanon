""""Convert the file StudentsMath_Score.sav into csv."""
import pandas as pd

FILE_NAME = 'StudentsMath_Score.sav'
NEW_FILE_NAME = 'StudentsMath_Score.csv'

df = pd.read_spss(FILE_NAME)
df.to_csv(NEW_FILE_NAME, index = False)
    
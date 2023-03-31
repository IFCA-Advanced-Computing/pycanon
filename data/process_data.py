"""Delete the rows of the dataset in which all QIs are set to *."""
import pandas as pd


def delete_rows(file_name, quasi_ident, new_file, fillna=True):
    """Delete the rows of the given file in which all QIs are set to *.
    Also fills NA values with 0."""
    df = pd.read_csv(file_name)
    df_qi = df[quasi_ident]
    df = df[:len(df_qi[df_qi != ['*'] * len(quasi_ident)].dropna(how='all'))]
    if fillna:
        df.fillna(0, inplace=True)
    df.to_csv(new_file, index=False)


QI = ['age', 'education', 'occupation', 'relationship', 'sex', 'native-country']
for i in [3, 10, 20]:
    file = f'./raw/adult_anonymized_{i}.csv'
    NEW_FILE_NAME = f'./processed/adult_anonymized_{i}.csv'
    delete_rows(file, QI, NEW_FILE_NAME)
    print(f'Saved file: {NEW_FILE_NAME}')

QI = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']
FILE_NAME = './raw/drug_type.csv'
NEW_FILE_NAME = './processed/drug_type.csv'
delete_rows(FILE_NAME, QI, NEW_FILE_NAME)
print(f'Saved file: {NEW_FILE_NAME}')

QI = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']
FILE_NAME = './raw/drugs_k5.csv'
NEW_FILE_NAME = './processed/drugs_k5.csv'
delete_rows(FILE_NAME, QI, NEW_FILE_NAME)
print(f'Saved file: {NEW_FILE_NAME}')

QI = ['name', 'age', 'gender', 'city']
FILE_NAME = './raw/hospital_anonymized.csv'
NEW_FILE_NAME = './processed/hospital_anonymized.csv'
delete_rows(FILE_NAME, QI, NEW_FILE_NAME)
print(f'Saved file: {NEW_FILE_NAME}')

QI = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type',
      'Residence_type', 'smoking_status']
FILE_NAME = './raw/healthcare-dataset-stroke-data.csv'
NEW_FILE_NAME = './processed/healthcare-dataset-stroke-data.csv'
delete_rows(FILE_NAME, QI, NEW_FILE_NAME)
print(f'Saved file: {NEW_FILE_NAME}')
for i in [2, 5, 10, 15, 19, 20, 22, 25]:
    FILE_NAME = f'./raw/stroke_k{i}.csv'
    NEW_FILE_NAME = f'./processed/stroke_k{i}.csv'
    delete_rows(FILE_NAME, QI, NEW_FILE_NAME)
    print(f'Saved file: {NEW_FILE_NAME}')

QI = ['Teacher', 'Gender', 'Ethnic', 'Freeredu', 'wesson']
FILE_NAME = './raw/StudentsMath_Score.csv'
NEW_FILE_NAME = './processed/StudentsMath_Score.csv'
delete_rows(FILE_NAME, QI, NEW_FILE_NAME)
df = pd.read_csv(NEW_FILE_NAME)
df[:-1].to_csv(NEW_FILE_NAME, index=False)  # all the values of the last row are 0
print(f'Saved file: {NEW_FILE_NAME}')
for i in [2, 5, 7]:
    FILE_NAME = f'./raw/StudentsMath_Score_k{i}.csv'
    NEW_FILE_NAME = f'./processed/StudentsMath_Score_k{i}.csv'
    delete_rows(FILE_NAME, QI, NEW_FILE_NAME)
    print(f'Saved file: {NEW_FILE_NAME}')

QI = ['Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class', 'Flight Distance',
      'Departure Delay in Minutes', 'Arrival Delay in Minutes']
FILE_NAME = './raw/airline_passenger_sat.csv'
NEW_FILE_NAME = './processed/airline_passenger_sat.csv'
delete_rows(FILE_NAME, QI, NEW_FILE_NAME)
print(f'Saved file: {NEW_FILE_NAME}')
for i in [2, 5, 10, 20]:
    FILE_NAME = f'./raw/airline_passenger_sat_k{i}.csv'
    NEW_FILE_NAME = f'./processed/airline_passenger_sat_k{i}.csv'
    delete_rows(FILE_NAME, QI, NEW_FILE_NAME)
    print(f'Saved file: {NEW_FILE_NAME}')

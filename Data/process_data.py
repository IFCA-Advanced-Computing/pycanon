# Delete the rows of the dataset in which all QIs are set to *.
import pandas as pd

def delete_rows(file, QI, new_file, delete_nan = True):
    df = pd.read_csv(file)
    df_QI = df[QI]
    n = len(df_QI[df_QI != ['*'] * len(QI)].dropna(how='all'))
    df = df[:n]
    if delete_nan:
        df.dropna(inplace = True)
    df.to_csv(new_file, index = False)
    
QI = ['age', 'education', 'occupation', 'relationship', 'sex', 'native-country']
for i in [3, 10, 20]:
    file = f'./Raw/adult_anonymized_{i}.csv'
    new_file = f'./Processed/adult_anonymized_{i}.csv'
    delete_rows(file, QI, new_file)
    print(f'Saved file: {new_file}')
    
QI = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']
file = './Raw/drug_type.csv'
new_file = f'./Processed/drug_type.csv'
delete_rows(file, QI, new_file)
print(f'Saved file: {new_file}')

QI = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']
file = './Raw/drugs_k5.csv'
new_file = f'./Processed/drugs_k5.csv'
delete_rows(file, QI, new_file)
print(f'Saved file: {new_file}')

QI = ['name', 'age', 'gender', 'city']
file = './Raw/hospital_anonymized.csv'
new_file = f'./Processed/hospital_anonymized.csv'
delete_rows(file, QI, new_file)
print(f'Saved file: {new_file}')

QI = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
file = './Raw/healthcare-dataset-stroke-data.csv'
new_file = f'./Processed/healthcare-dataset-stroke-data.csv'
delete_rows(file, QI, new_file)
print(f'Saved file: {new_file}')
for i in [2, 5, 10, 20]:
    file = f'./Raw/stroke_k{i}.csv'
    new_file = f'./Processed/stroke_k{i}.csv'
    delete_rows(file, QI, new_file)
    print(f'Saved file: {new_file}')
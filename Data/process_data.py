# Delete the rows of the dataset in which all QIs are set to *.
import pandas as pd

def delete_rows(file, QI, new_file, fillna = True):
    df = pd.read_csv(file)
    df_QI = df[QI]
    n = len(df_QI[df_QI != ['*'] * len(QI)].dropna(how='all'))
    df = df[:n]
    if fillna:
        df.fillna(0, inplace = True)
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
for i in [2, 5, 10, 15, 19, 20, 22, 25]:
    file = f'./Raw/stroke_k{i}.csv'
    new_file = f'./Processed/stroke_k{i}.csv'
    delete_rows(file, QI, new_file)
    print(f'Saved file: {new_file}')
    
QI = ['Teacher', 'Gender', 'Ethnic', 'Freeredu', 'wesson']
file = './Raw/StudentsMath_Score.csv'
new_file = f'./Processed/StudentsMath_Score.csv'
delete_rows(file, QI, new_file)
df = pd.read_csv(new_file)
df[:-1].to_csv(new_file, index = False) # Se quita la última fila que tiene todos los valores como 0
print(f'Saved file: {new_file}')
for i in [2, 5, 7]:
    file = f'./Raw/StudentsMath_Score_k{i}.csv'
    new_file = f'./Processed/StudentsMath_Score_k{i}.csv'
    delete_rows(file, QI, new_file)
    print(f'Saved file: {new_file}')
    
    
QI = ['Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class', 'Flight Distance', 'Departure Delay in Minutes', 'Arrival Delay in Minutes']
file = './Raw/airline_passenger_sat.csv'
new_file = f'./Processed/airline_passenger_sat.csv'
delete_rows(file, QI, new_file)
print(f'Saved file: {new_file}')
for i in [2, 5, 10, 20]:
    file = f'./Raw/airline_passenger_sat_k{i}.csv'
    new_file = f'./Processed/airline_passenger_sat_k{i}.csv'
    delete_rows(file, QI, new_file)
    print(f'Saved file: {new_file}')

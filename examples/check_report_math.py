"""Example of the function: get_anon_report(), using the student's math score dataset."""

import pandas as pd
from pycanon.report import json, pdf

QI = ['Teacher', 'Gender', 'Ethnic', 'Freeredu', 'wesson']
FILE_NAME_1 = './data/processed/StudentsMath_Score.csv'
DATA_1 = pd.read_csv(FILE_NAME_1)
SA = ['Score']
FILE_PDF_1 = 'test_math.pdf'
FILE_JSON_1 = 'test_math.json'

print(json.get_json_report(DATA_1, QI, SA))
pdf.get_pdf_report(DATA_1, QI, SA, file_pdf=FILE_PDF_1)

FILE_NAME_2 = './data/processed/StudentsMath_Score_k5.csv'
DATA_2 = pd.read_csv(FILE_NAME_2)
FILE_PDF_2 = 'test_math_k5.pdf'
FILE_JSON_2 = 'test_math_k5.json'
print(json.get_json_report(DATA_2, QI, SA))
pdf.get_pdf_report(DATA_2, QI, SA)

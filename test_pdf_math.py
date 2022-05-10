"""Example of the function: get_anon_report(), using the student's math score dataset."""
from pycanon import test_anonymity

QI = ['Teacher', 'Gender', 'Ethnic', 'Freeredu', 'wesson']
FILE_NAME = './Data/Processed/StudentsMath_Score.csv'
SA = ['Score']
FILE_PDF = 'test_math.pdf'
test_anonymity.get_anon_report(FILE_NAME, QI, SA, file_pdf = FILE_PDF)

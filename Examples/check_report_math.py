"""Example of the function: get_anon_report(), using the student's math score dataset."""

from pycanon import report

QI = ['Teacher', 'Gender', 'Ethnic', 'Freeredu', 'wesson']
FILE_NAME_1 = './Data/Processed/StudentsMath_Score.csv'
SA = ['Score']
FILE_PDF_1 = 'test_math.pdf'
FILE_JSON_1 = 'test_math.json'

report.print_report(FILE_NAME_1, QI, SA)
print(report.get_json_report(FILE_NAME_1, QI, SA))
report.get_pdf_report(FILE_NAME_1, QI, SA, file_pdf = FILE_PDF_1)

FILE_NAME_2 = './Data/Processed/StudentsMath_Score_k5.csv'
FILE_PDF_2 = 'test_math_k5.pdf'
FILE_JSON_2 = 'test_math_k5.json'
report.print_report(FILE_NAME_2, QI, SA)
print(report.get_json_report(FILE_NAME_2, QI, SA)
report.get_pdf_report(FILE_NAME_2, QI, SA)

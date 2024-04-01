# importing pandas module
import pandas as pd

# reading the csv file
cvsDataframe = pd.read_csv('Amtran_out.csv')

# creating an output excel file
resultExcelFile = pd.ExcelWriter('ResultExcelFile.xlsx')

# converting the csv file to an excel file
cvsDataframe.to_excel(resultExcelFile, index=False)

# saving the excel file
resultExcelFile.save()
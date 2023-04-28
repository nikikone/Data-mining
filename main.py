from DataMining import *
import xlsxwriter as xls

attributeSize = 12
classSize = 5
ibSize = 10

a = DataMining(attributeSize)
a.AttributeGeneration()
a.ClassGeneration(classSize)
path="data\\"
name="MBZ.xlsx"
workbook = xls.Workbook(path + name) # Создать файл
a.MVD(ibSize)
a.ToExcelMBZ(workbook)
a.ToExcelMVD(workbook)
#a.IfbzBorderDelimiter()
#a.IfbzBorderSummator()
workbook.close()
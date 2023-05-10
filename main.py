from DataMining import *
import xlsxwriter as xls

attributeSize = 12
classSize = 1
ibSize = 20

a = DataMining(attributeSize, numSatke=0)
a.AttributeGeneration()
a.ClassGeneration(classSize)
path="data\\"
name="MBZ.xlsx"
workbook = xls.Workbook(path + name) # Создать файл
a.MVD(ibSize)
a.ToExcelMBZ(workbook)
a.ToExcelMVD(workbook)
workbook.close()
a.IfbzBorderDelimiter()
a.IfbzBorderSummator()
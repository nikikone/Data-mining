from DataMining import *
import xlsxwriter as xls

attributeSize = 3
classSize = 1
ibSize = 300

a = DataMining(attributeSize, numSatke=0, katStake=0)
a.AttributeGeneration()
a.ClassGeneration(classSize)
path="data\\"
name="MBZ.xlsx"
workbook = xls.Workbook(path + name) # Создать файл
a.MVD(ibSize)
a.ToExcelMBZ(workbook)
a.ToExcelMVD(workbook)
a.IfbzBorderDelimiter()
a.IfbzBorderSummator()
a.ToExcelMBZvsIFBZ(workbook)
workbook.close()
#a.ToExcelIFBZ()
from DataMining import *
import xlsxwriter as xls

attributeSize = 3
classSize = 2
ibSize = 50

a = DataMining(attributeSize)
a.AttributeGeneration()
a.ClassGeneration(classSize)
path="" # Путь к папке формата "data\\"
name="MBZ, MVD, IFBZ, MBZ vs IFBZ.xlsx"
workbook = xls.Workbook(path + name) # Создать файл
a.MVD(ibSize)
a.ToExcelMBZ(workbook)
a.ToExcelMVD(workbook)
a.IfbzBorderDelimiter()
a.IfbzBorderSummator()

a.ToExcelIFBZ(workbook)

a.ToExcelMBZvsIFBZ(workbook)
workbook.close()
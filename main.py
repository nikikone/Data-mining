from MBZ import *
import xlsxwriter as xls

a = MBZ(3)
a.AttributeGeneration()
a.ClassGeneration(2)
path="data\\"
name="MBZ.xlsx"
workbook = xls.Workbook(path + name) # Создать файл
a.MVD(5)
a.ToExcelMBZ(workbook)
a.ToExcelMVD(workbook)
a.IfbzBorderDelimiter()

workbook.close()
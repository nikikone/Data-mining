import numpy as np
import pandas as pd
import xlsxwriter
#d = {'col1': [1, 2], 'col2': [3, 4]}
#d2 = {'col1': [3, 4], 'col2': [5, 6]}
#df = pd.DataFrame(data=d)
#df2 = pd.DataFrame(data=d2)
#writer = pd.ExcelWriter('data\\example.xlsx', engine='xlsxwriter')
## Записать ваш DataFrame в файл     
#df.to_excel(writer, 'Sheet1')
#df2.to_excel(writer, 'Sheet1')
## Сохраним результат 
#writer.save()
workbook = xlsxwriter.Workbook('data\\hello.xlsx') # Создать файл
worksheet = workbook.add_worksheet() # Создать лист, вы можете указать имя листа с помощью work.add_worksheet ('employee'), но китайское имя будет сообщать об ошибке UnicodeDecodeErro
expenses = (
    ['Rent', 1000],
    ['Gas',   100],
    ['Food',  300],
    ['Gym',    50],
)
  
# Начать с первой ячейки. Строки и столбцы индексируются нулем. Запись по метке начинается с 0, а запись по абсолютной позиции "A1" начинается с 1
row = 0
col = 0
  
# Iterate over the data and write it out row by row.
for item, cost in (expenses):
    worksheet.write(row, col,     item)
    worksheet.write(row, col + 1, cost)
    row += 1
  
# Write a total using a formula.
worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, '=SUM(B1:B4)')    # Вызываем формульное выражение excel
  
workbook.close()

#attribute = np.zeros((2))
#print(attribute)
#attribute[0] = [1, 1]
#print(attribute)
#attrSize = 8
#
#numS = 2
#binS = 2
#katS = 2
#stake = numS + binS + katS
#colNum = numS * (attrSize / 2)
#test = (1, 2)
#test_2 = [3, 2, 1, 3]
#test_3 = (test, test_2)
#c = np.intersect1d(test, test_2)
#print(test_3)
#print(test @ test_2)
#print(type(test_3) is list)
#print(np.random.randint(*test, 2))
#for i in range(30):
#    print(np.random.randint(0, 2))
#print(test_3[test])
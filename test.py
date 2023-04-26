import numpy as np
import itertools
#import pandas as pd
#import xlsxwriter

testSlov = set([1, 2, 3])
testSlov_2 = set([3, 2, 5])
testSlov_3 = testSlov.union(testSlov_2)
print(testSlov_3)


#mas = [(3, 8), (8, 8), (12, 4), (22, 1), (32, 6), (34, 9)]
##mas = [(3, 1), (8, 1), (12, 1), (22, 0), (32, 1), (34, 0)]
##mas = [(3, 8), (8, 8), (12, 4), (22, 1)]
#
#npMas = np.array(mas)
#masK = [i for i in range(len(mas))]
#masProv = npMas[:, 1]
##print(masK)
#result = []
#numOfPd = 4
#a = itertools.combinations(masK, numOfPd)
#for i in a:
#    flag = True
#    resOut = []
#    if numOfPd >= 2:
#        left = 0
#        right = len(mas)
#        for iterPD in range(1, len(i)):
#            #print(i, masProv[i[iterPD]:i[1 + iterPD]], masProv[i[1 + iterPD]:i[2 + iterPD]], "-", i[0 + iterPD: 1 + iterPD], i[1 + iterPD: 2 + iterPD])
#            #print()
#            if iterPD == 1:
#                left = 0
#            else:
#                left = i[iterPD - 1]
#            if iterPD == len(i) - 1:
#                right = len(mas)
#            else:
#                right = i[iterPD + 1]
#            mas_1 = set(masProv[left:i[iterPD]])
#            mas_2 = set(masProv[i[iterPD]:right])
#            #print(i, mas_1, " - ", mas_2)
#            #print(i[iterPD], right)
#            #print(left, i[iterPD], ":", i[iterPD], right)
#            string = "[" + str(npMas[i[iterPD] - 1, 0]) + ", " + str(npMas[i[iterPD], 0]) + ")"
#            resOut.append(string)
#            if not mas_1.isdisjoint(mas_2):
#                #print("Не соответствует")
#                flag = False
#                break
#        #print()
#    if flag and resOut not in result:
#        result.append(resOut)
#print(result)
#for k in range(1, len(mas)):
#    mas_1 = mas[:k]
#    mas_2 = mas[k:]
#    mnoz_1 = set()
#    mnoz_2 = set()
#    for mn, value in mas_1:
#        mnoz_1.add(value)
#    for mn, value in mas_2:
#        mnoz_2.add(value)
#    if mnoz_1.isdisjoint(mnoz_2):
#        print(mas[k][0])



for i in range(1, 5):
    pass


#maxIndex = len(mas) - 1
#minIndex = 1
#for i in range(maxIndex):
#    masOfIter = []
#    masOfIter.extend([1]*minIndex)
#    masOfIter.extend([0]*(maxIndex - minIndex + 1))
#    for k in range(len(masOfIter)):
#        
#        pass
#masOfIter = np.array(masOfIter)
#mas = np.array(mas)
#print(mas[masOfIter > 0])



#mas = {}
#mas[1] = 2
#mas['2'] = 1
#print(mas[3])

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
#workbook = xlsxwriter.Workbook('data\\hello.xlsx') # Создать файл
#worksheet = workbook.add_worksheet() # Создать лист, вы можете указать имя листа с помощью work.add_worksheet ('employee'), но китайское имя будет сообщать об ошибке UnicodeDecodeErro
#expenses = (
#    ['Rent', 1000],
#    ['Gas',   100],
#    ['Food',  300],
#    ['Gym',    50],
#)
  
# Начать с первой ячейки. Строки и столбцы индексируются нулем. Запись по метке начинается с 0, а запись по абсолютной позиции "A1" начинается с 1
#row = 0
#col = 0
  
# Iterate over the data and write it out row by row.
#for item, cost in (expenses):
#    worksheet.write(row, col,     item)
#    worksheet.write(row, col + 1, cost)
#    row += 1
  
# Write a total using a formula.
#worksheet.write(row, 0, 'Total')
#worksheet.write(row, 1, '=SUM(B1:B4)')    # Вызываем формульное выражение excel
#  
#workbook.close()

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
import numpy as np
import xlsxwriter as xls

SIZE_KATEGORIAL_CONSTANT = 10
LEFT_NUM_CONSTANT = 0
RIGHT_NUM_CONSTANT = 1000
LEFT_CHPD_CONSTANT = 1
RIGHT_CHPD_CONSTANT = 5
MINIMUM_LENGTH_NUM = 60

# classValues
[ # <- Классы (Заболевания)
    [ # <- Признаки
        ( # <- Значения признака в периодах динамики / (Нижняя граница, Верхняя граница) кол-ва моментов наблюдения
            [ # <- Массив кортежей, списков или чисел
    
            ],
            [ # < - Кортежи (НГ, ВГ)
    
            ]
        )
    ]
]
# TODO Придумать другой вариант хранения данных МВД, т.к. текущий плох в плане повторения уже имеющихся данных
# mvdValues
[ # <- Классы (Заболевания)
    [ # <- Признаки
        ( # <- Значения признака в периодах динамики / (Нижняя граница, Верхняя граница) кол-ва длительности ПД
            [ # <- Массив кортежей, списков или чисел
    
            ],
            [ # < - Кортежи (Длительность ПД, Число МН)
    
            ]
        )
    ]
]

class MBZ:
    def __init__(self, attr, *, katStake=1, binStake=1, numSatke=1) -> None:
        self.attributeSize = attr
        self.katStake = katStake
        self.binStake = binStake
        self.numStake = numSatke

    def AttributeGeneration(self):
        stake = self.katStake + self.binStake + self.numStake
        persentStake = self.attributeSize // (stake)
        remain = np.zeros((3))
        for i in range(self.attributeSize % stake):
            remain[i] = 1
        
        numSize = int(self.numStake * persentStake + remain[0])
        katSize = int(self.katStake * persentStake + remain[1])
        binSize = int(self.binStake * persentStake + remain[2])
        self.attributePossibleValues = []
        self.attributeNormalValues = []

        for _ in range(numSize):
            rand_num = [0, 0]
            while abs(rand_num[1] - rand_num[0]) < MINIMUM_LENGTH_NUM:
                rand_num = np.random.randint(LEFT_NUM_CONSTANT, RIGHT_NUM_CONSTANT + 1, 2)
            self.attributePossibleValues.append((np.min(rand_num), np.max(rand_num)))
            rand_num = np.random.randint(np.min(rand_num), np.max(rand_num) + 1, 2)
            self.attributeNormalValues.append((np.min(rand_num), np.max(rand_num)))
        
        for _ in range(katSize):
            kategorialSize = np.random.randint(2, SIZE_KATEGORIAL_CONSTANT + 1)
            kategorial, normKategorial = [], []    
            for i in range(1, kategorialSize + 1):
                kategorial.append(i)
            self.attributePossibleValues.append(kategorial.copy())
            if kategorialSize - 1 == 1:
                numberNormalValues = 1    
            else:
                numberNormalValues = np.random.randint(1, kategorialSize - 1)
            for i in range(numberNormalValues):
                random_index = np.random.randint(0, len(kategorial))
                normKategorial.append(kategorial[random_index])
                kategorial.pop(random_index)
            self.attributeNormalValues.append(normKategorial)
        
        for _ in range(binSize):
            self.attributePossibleValues.append(1)
            self.attributeNormalValues.append(np.random.randint(0, 2))

    def ClassGeneration(self, classSize):
        RATIO = 1.2
        self.classSize = classSize
        self.classValues = []
        for numClass in range(classSize):
            mas = []
            for numAttribute in range(self.attributeSize):
                rest = [0] * np.random.randint(LEFT_CHPD_CONSTANT, RIGHT_CHPD_CONSTANT + 1)
                upAndDownBorder = [0] * len(rest)
                for numPD in range(len(rest)):
                    upAndDownBorder[numPD] = np.random.randint(1, 25, 2)
                    upAndDownBorder[numPD] = (np.min(upAndDownBorder[numPD]), np.max(upAndDownBorder[numPD]))
                    if type(self.attributePossibleValues[numAttribute]) is tuple:
                        checkDifference = False
                        while True:
                            thisPD = np.random.randint(*self.attributePossibleValues[numAttribute], 2)
                            thisPD = (np.min(thisPD), np.max(thisPD))
                            if numPD > 0 and not (rest[numPD - 1][1] < thisPD[0] or thisPD[1] < rest[numPD - 1][0]) :
                                checkDifference = False
                            else:
                                checkDifference = True
                            if checkDifference and (self.attributePossibleValues[numAttribute][1] - self.attributePossibleValues[numAttribute][0]) \
                                 % (thisPD[1] - thisPD[0]) > RATIO:
                                break
                        rest[numPD] = thisPD
                        # Остановился здесь, планировал перегрузить оператор @ для работы с кортежами, но передумал
                        # Здась требуется создать значения для периодов так, чтобы соседние не пересекались
                    elif type(self.attributePossibleValues[numAttribute]) is list:
                        while True:
                            shufflMas = np.array(self.attributePossibleValues[numAttribute])
                            np.random.shuffle(shufflMas)
                            num = np.random.randint(1, len(shufflMas) // 2 + 1)
                            thisPD = shufflMas[:num].tolist()
                            if numPD > 0 and len(np.intersect1d(thisPD, rest[numPD - 1])) == 0:
                                break
                            elif numPD == 0:
                                break
                        rest[numPD] = thisPD
                    elif type(self.attributePossibleValues[numAttribute]) is int:
                        if numPD == 0:
                            rest[0] = np.random.randint(0, 2)
                        else:
                            rest[numPD] = 1 - rest[numPD - 1]
                mas.append((rest, upAndDownBorder))
            self.classValues.append(mas)
    
    def ToExcel(self, *, path="data\\", name="MBZ.xlsx"):
        workbook = xls.Workbook(path + name) # Создать файл
        worksheet = workbook.add_worksheet('МБЗ') # Создать лист

        column = 0
        worksheet.write(0, 0, "Заболевания")
        for row in range(1, self.classSize + 1):
            worksheet.write(row, column, "Заболевание " + str(row))
        worksheet.set_column(column, column, 15)

        column += 2
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.write(0, column, "Признаки")
        for row in range(1, self.attributeSize + 1):
            worksheet.write(row, column, "Признак " + str(row))
        worksheet.set_column(column, column, 10)

        column += 2
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 1, "Возможные значения (ВЗ)")
        for row in range(1, self.attributeSize + 1):
            worksheet.write(row, column, "Признак " + str(row))
            if type(self.attributePossibleValues[row - 1]) is tuple:
                left, right = self.attributePossibleValues[row - 1]
                worksheet.write(row, column + 1, '[' + str(int(left)) + '-' + str(int(right)) + ']')
            elif type(self.attributePossibleValues[row - 1]) is list:
                listAttrRow = '{'
                for i in range(len(self.attributePossibleValues[row - 1])):
                    listAttrRow += "значение " + str(i + 1) + ", "
                listAttrRow = listAttrRow[:-2] + '}'
                worksheet.write(row, column + 1, listAttrRow)
            elif type(self.attributePossibleValues[row - 1]) is int:
                worksheet.write(row, column + 1, "(0, 1)")
        worksheet.set_column(column, column, 12)
        worksheet.set_column(column + 1, column + 1, 12)

        column += 3
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 1, "Нормальные значения (НЗ)")
        for row in range(1, self.attributeSize + 1):
            worksheet.write(row, column, "Признак " + str(row))
            if type(self.attributeNormalValues[row - 1]) is tuple:
                first, second = self.attributeNormalValues[row - 1]
                worksheet.write(row, column + 1, '[' + str(int(first)) + '-' + str(int(second)) + ']')
            elif type(self.attributeNormalValues[row - 1]) is list:
                listAttrRow = '{'
                for i in range(len(self.attributeNormalValues[row - 1])):
                    listAttrRow += "значение " + str(i + 1) + ", "
                listAttrRow = listAttrRow[:-2] + '}'
                worksheet.write(row, column + 1, listAttrRow)
            elif type(self.attributeNormalValues[row - 1]) is int:
                worksheet.write(row, column + 1, self.attributeNormalValues[row - 1])
        worksheet.set_column(column, column, 12)
        worksheet.set_column(column + 1, column + 1, 12)

        column += 3
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 1, "Клиническая картина (КК)")
        stepRow = 0
        for i in range(self.classSize):
            worksheet.merge_range(1 + stepRow, column, stepRow + self.attributeSize, column, "Заболевание " + str(i + 1))
            for j in range(self.attributeSize):
                worksheet.write(j + 1 + stepRow, column + 1, "Признак " + str(j + 1))
            stepRow += self.attributeSize
        worksheet.set_column(column, column, 15)
        worksheet.set_column(column + 1, column + 1, 14)

        column += 3
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 2, "Число периодов динамики (ЧПД)")
        iterRow = 0
        for classIter in range(self.classSize):
            for attrIter in range(self.attributeSize):
                chPD = len(self.classValues[classIter][attrIter][0])
                worksheet.write(1 + iterRow, column, "Заболевание " + str(classIter + 1))
                worksheet.write(1 + iterRow, column + 1, "Признак " + str(attrIter + 1))
                worksheet.write(1 + iterRow, column + 2, chPD)
                iterRow += 1
        worksheet.set_column(column, column, 15)
        worksheet.set_column(column + 1, column + 1, 12)
        worksheet.set_column(column + 2, column + 2, 12)
        
        column += 4
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 3, "Значение для периода (ЗДП)")
        iterRow = 0
        for classIter in range(self.classSize):
            for attrIter in range(self.attributeSize):
                chPD = len(self.classValues[classIter][attrIter][0])
                for PD in range(chPD):
                    worksheet.write(1 + iterRow, column, "Заболевание " + str(classIter + 1))
                    worksheet.write(1 + iterRow, column + 1, "Признак " + str(attrIter + 1))
                    worksheet.write(1 + iterRow, column + 2, PD + 1)
                    if type(self.attributeNormalValues[attrIter]) is tuple:
                        left, right = self.classValues[classIter][attrIter][0][PD]
                        outPutRow = '[' + str(int(left)) + '-' + str(int(right)) + ']'
                    elif type(self.attributeNormalValues[attrIter]) is list:
                        outPutRow = ''
                        for i in range(len(self.classValues[classIter][attrIter][0][PD])):
                            outPutRow += 'значение ' + str(self.classValues[classIter][attrIter][0][PD][i]) + ', '
                        outPutRow = outPutRow[:-2]
                    elif type(self.attributeNormalValues[attrIter]) is int:
                        outPutRow = self.classValues[classIter][attrIter][0][PD]
                    worksheet.write(1 + iterRow, column + 3, outPutRow)
                    iterRow += 1
        worksheet.set_column(column, column, 15)
        worksheet.set_column(column + 1, column + 1, 12)
        worksheet.set_column(column + 2, column + 2, 12)
        worksheet.set_column(column + 2, column + 2, 12)

        column += 5
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 3, "Верхние и нижние границы (ВГ и НГ)")
        iterRow = 0
        for classIter in range(self.classSize):
            for attrIter in range(self.attributeSize):
                chPD = len(self.classValues[classIter][attrIter][0])
                for PD in range(chPD):
                    worksheet.write(1 + iterRow, column, "Заболевание " + str(classIter + 1))
                    worksheet.write(1 + iterRow, column + 1, "Признак " + str(attrIter + 1))
                    worksheet.write(1 + iterRow, column + 2, self.classValues[classIter][attrIter][1][PD][1])
                    worksheet.write(1 + iterRow, column + 3, self.classValues[classIter][attrIter][1][PD][0])
                    iterRow += 1
        worksheet.set_column(column, column, 15)
        worksheet.set_column(column + 1, column + 1, 12)
        worksheet.set_column(column + 2, column + 2, 12)
        worksheet.set_column(column + 2, column + 2, 12)

        workbook.close()

    def MVD(self):
        pass
        
#a = MBZ(3)
#a.AttributeGeneration()
#a.ClassGeneration(1)
##print(a.classValues)
##print(a.attributePossibleValues)
#a.ToExcel()
#print(a.attributeNormalValues)

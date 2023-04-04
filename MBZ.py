import numpy as np
import xlsxwriter as xls


# Границы кол-ва ПД
LEFT_CHPD_CONSTANT = 1
RIGHT_CHPD_CONSTANT = 5

# Границы моментов наблюдения
LEFT_MN_CONSTANT = 1 # 
RIGHT_MN_CONSTANT = 3 #

# Границы возможных значений числовых признаков
LEFT_NUM_CONSTANT = 0
RIGHT_NUM_CONSTANT = 1000

# Максимальное кол-во значений категориальных признаков
SIZE_KATEGORIAL_CONSTANT = 10

# Минимальное расстояние между левой и правой границами возможных значений признаков
MINIMUM_LENGTH_NUM = 60


# classValues
[ # <- Классы (Заболевания)
    [ # <- Признаки
        ( # <- Значения признака в периодах динамики / (Нижняя граница, Верхняя граница) кол-ва моментов наблюдения
            [ # <- Массив кортежей, списков или чисел, <- Значения признака в периодах динамики
                [ # <- значения в ПД (tuple, list или int)
    
                ]
            ],
            [ # < - Кортежи (НГ, ВГ)
                [ # <- Значения в ПД
    
                ]
            ]
        )
    ]
]

# pdMnValues
[ # <- Классы (Заболевания)
    [ # <- Истории болезни (ИБ)
        [ # <- Признаки
            [ # <- ПД
                ( # <- Длительность и число МН
    
                )
            ]
        ]
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
    
    def ToExcelMBZ(self, workbook): # path="data\\", name="MBZ.xlsx"
        Format = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': '#FBD4B4', 'border': 1})
        FormatBold = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': '#FBD4B4', 'border': 1, 'bold': True})
        worksheet = workbook.add_worksheet('МБЗ') # Создать лист
        column = 0
        worksheet.write(0, 0, "Заболевания", FormatBold)
        for row in range(1, self.classSize + 1):
            worksheet.write(row, column, "Заболевание " + str(row), Format)
        worksheet.set_column(column, column, 15)

        column += 2
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.write(0, column, "Признаки", FormatBold)
        for row in range(1, self.attributeSize + 1):
            worksheet.write(row, column, "Признак " + str(row), Format)
        worksheet.set_column(column, column, 10)

        column += 2
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 1, "Возможные значения (ВЗ)", FormatBold)
        for row in range(1, self.attributeSize + 1):
            worksheet.write(row, column, "Признак " + str(row), Format)
            if type(self.attributePossibleValues[row - 1]) is tuple:
                left, right = self.attributePossibleValues[row - 1]
                worksheet.write(row, column + 1, '[' + str(int(left)) + '-' + str(int(right)) + ']', Format)
            elif type(self.attributePossibleValues[row - 1]) is list:
                listAttrRow = '{'
                for i in range(len(self.attributePossibleValues[row - 1])):
                    listAttrRow += "значение " + str(i + 1) + ", "
                listAttrRow = listAttrRow[:-2] + '}'
                worksheet.write(row, column + 1, listAttrRow, Format)
            elif type(self.attributePossibleValues[row - 1]) is int:
                worksheet.write(row, column + 1, "(0, 1)", Format)
        worksheet.set_column(column, column, 12)
        worksheet.set_column(column + 1, column + 1, 12)

        column += 3
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 1, "Нормальные значения (НЗ)", FormatBold)
        for row in range(1, self.attributeSize + 1):
            worksheet.write(row, column, "Признак " + str(row), Format)
            if type(self.attributeNormalValues[row - 1]) is tuple:
                first, second = self.attributeNormalValues[row - 1]
                worksheet.write(row, column + 1, '[' + str(int(first)) + '-' + str(int(second)) + ']', Format)
            elif type(self.attributeNormalValues[row - 1]) is list:
                listAttrRow = '{'
                for i in range(len(self.attributeNormalValues[row - 1])):
                    listAttrRow += "значение " + str(i + 1) + ", "
                listAttrRow = listAttrRow[:-2] + '}'
                worksheet.write(row, column + 1, listAttrRow, Format)
            elif type(self.attributeNormalValues[row - 1]) is int:
                worksheet.write(row, column + 1, self.attributeNormalValues[row - 1], Format)
        worksheet.set_column(column, column, 12)
        worksheet.set_column(column + 1, column + 1, 12)

        column += 3
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 1, "Клиническая картина (КК)", FormatBold)
        stepRow = 0
        for i in range(self.classSize):
            worksheet.merge_range(1 + stepRow, column, stepRow + self.attributeSize, column, "Заболевание " + str(i + 1), Format)
            for j in range(self.attributeSize):
                worksheet.write(j + 1 + stepRow, column + 1, "Признак " + str(j + 1), Format)
            stepRow += self.attributeSize
        worksheet.set_column(column, column, 15)
        worksheet.set_column(column + 1, column + 1, 14)

        column += 3
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 2, "Число периодов динамики (ЧПД)", FormatBold)
        iterRow = 0
        for classIter in range(self.classSize):
            for attrIter in range(self.attributeSize):
                chPD = len(self.classValues[classIter][attrIter][0])
                worksheet.write(1 + iterRow, column, "Заболевание " + str(classIter + 1), Format)
                worksheet.write(1 + iterRow, column + 1, "Признак " + str(attrIter + 1), Format)
                worksheet.write(1 + iterRow, column + 2, chPD, Format)
                iterRow += 1
        worksheet.set_column(column, column, 15)
        worksheet.set_column(column + 1, column + 1, 12)
        worksheet.set_column(column + 2, column + 2, 12)
        
        column += 4
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 3, "Значение для периода (ЗДП)", FormatBold)
        iterRow = 0
        for classIter in range(self.classSize):
            for attrIter in range(self.attributeSize):
                chPD = len(self.classValues[classIter][attrIter][0])
                for PD in range(chPD):
                    worksheet.write(1 + iterRow, column, "Заболевание " + str(classIter + 1), Format)
                    worksheet.write(1 + iterRow, column + 1, "Признак " + str(attrIter + 1), Format)
                    worksheet.write(1 + iterRow, column + 2, PD + 1, Format)
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
                    worksheet.write(1 + iterRow, column + 3, outPutRow, Format)
                    iterRow += 1
        worksheet.set_column(column, column, 15)
        worksheet.set_column(column + 1, column + 1, 12)
        worksheet.set_column(column + 2, column + 2, 12)
        worksheet.set_column(column + 2, column + 2, 12)

        column += 5
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 3, "Верхние и нижние границы (ВГ и НГ)", FormatBold)
        iterRow = 0
        for classIter in range(self.classSize):
            for attrIter in range(self.attributeSize):
                chPD = len(self.classValues[classIter][attrIter][0])
                for PD in range(chPD):
                    worksheet.write(1 + iterRow, column, "Заболевание " + str(classIter + 1), Format)
                    worksheet.write(1 + iterRow, column + 1, "Признак " + str(attrIter + 1), Format)
                    worksheet.write(1 + iterRow, column + 2, self.classValues[classIter][attrIter][1][PD][1], Format)
                    worksheet.write(1 + iterRow, column + 3, self.classValues[classIter][attrIter][1][PD][0], Format)
                    iterRow += 1
        worksheet.set_column(column, column, 15)
        worksheet.set_column(column + 1, column + 1, 12)
        worksheet.set_column(column + 2, column + 2, 12)
        worksheet.set_column(column + 2, column + 2, 12)
        

    def MVD(self, IbSize):
        self.IbSize = IbSize
        pdMnValues = []
        for classIter in range(self.classSize):
            ibMass = []
            for IbIter in range(self.IbSize):
                attrMass = []
                for attrIter in range(self.attributeSize):
                    pdMass = []
                    chPD = len(self.classValues[classIter][attrIter][0])
                    for PD in range(chPD):
                        downBorder, uppBorder = self.classValues[classIter][attrIter][1][PD]
                        if downBorder == uppBorder:
                            durationPD = downBorder
                        else:
                            durationPD = np.random.randint(downBorder, uppBorder + 1)
                        if durationPD <= LEFT_MN_CONSTANT:
                            chMN = durationPD
                        else:
                            chMN = np.random.randint(LEFT_MN_CONSTANT, min(RIGHT_MN_CONSTANT, durationPD) + 1)
                        pdMass.append((durationPD, chMN))
                    attrMass.append(pdMass)
                ibMass.append(attrMass)
            pdMnValues.append(ibMass)
        self.pdMnValues = pdMnValues


    
    def ToExcelMVD(self, workbook):
        worksheet = workbook.add_worksheet('МВД')
        Format = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': '#FBD4B4', 'border': 1})
        FormatBold = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': '#FBD4B4', 'border': 1, 'bold': True})
        column = 0
        worksheet.merge_range(0, column, 0, column + 5, "(ИБ, заболевание, признак, номер ПД, длительность ПД, число МН в ПД)", FormatBold)
        iterRow = 1
        for classIter in range(self.classSize):
            for IbIter in range(self.IbSize):
                rowClassLen = 0
                for attrIter in range(self.attributeSize):
                    pdSize = len(self.pdMnValues[classIter][IbIter][attrIter])
                    for PD in range(pdSize):
                        durationPD, chMN = self.pdMnValues[classIter][IbIter][attrIter][PD]
                        worksheet.write(iterRow, column + 3, PD + 1, Format)
                        worksheet.write(iterRow, column + 4, durationPD, Format)
                        worksheet.write(iterRow, column + 5, chMN, Format)
                        iterRow += 1
                    if pdSize != 1:
                        worksheet.merge_range(iterRow - pdSize, column + 2, iterRow - 1, column + 2, "Признак " + str(attrIter + 1), Format)
                    else:
                        worksheet.write(iterRow - 1, column + 2, "Признак " + str(attrIter + 1), Format)
                    rowClassLen += pdSize
                worksheet.merge_range(iterRow - rowClassLen, column + 1, iterRow - 1, column + 1, "Заболевание " + str(classIter + 1), Format)
                worksheet.merge_range(iterRow - rowClassLen, column, iterRow - 1, column, "ИБ " + str(IbIter + 1), Format)
        
        column += 7
        iterRow = 1
        worksheet.merge_range(0, column, 0, column + 4, "Выборка данных (ИБ, заболевание, признак, МН, значение в МН)", FormatBold)
        for classIter in range(self.classSize):
            for IbIter in range(self.IbSize):
                rowClassLen = 0
                for attrIter in range(self.attributeSize):
                    rowAttrLen = 0
                    pdSize = len(self.pdMnValues[classIter][IbIter][attrIter])
                    summatorPD = 0
                    for PD in range(pdSize):
                        durationPD, chMN = self.pdMnValues[classIter][IbIter][attrIter][PD]
                        leftDurationMN, rightDurationNM = 1, durationPD - chMN + 2 # Поменять на + 1, если ВГ не надо касаться ВГ
                        rowAttrLen += chMN
                        for MN in range(chMN):
                            valueInPD = self.classValues[classIter][attrIter][0][PD]
                            if type(valueInPD) is tuple:
                                valueInMN = int(np.random.randint(*valueInPD))
                                worksheet.write(iterRow, column + 4, valueInMN, Format)
                            elif type(valueInPD) is list:
                                indexValueKategorial = int(np.random.randint(0, len(valueInPD)))
                                worksheet.write(iterRow, column + 4, "значение " + str(valueInPD[indexValueKategorial]), Format)
                            elif type(valueInPD) is int:
                                worksheet.write(iterRow, column + 4, valueInPD, Format)
                            if leftDurationMN < rightDurationNM - 1:
                                mn = int(np.random.randint(leftDurationMN, rightDurationNM))
                            else:
                                mn = leftDurationMN
                            worksheet.write(iterRow, column + 3, mn + summatorPD, Format)
                            leftDurationMN, rightDurationNM = mn + 1, rightDurationNM + 1
                            iterRow += 1
                        summatorPD += durationPD
                    if rowAttrLen != 1:
                            worksheet.merge_range(iterRow - rowAttrLen, column + 2, iterRow - 1, column + 2, "Признак " + str(attrIter + 1), Format)
                    else:
                        worksheet.write(iterRow - 1, column + 2, "Признак " + str(attrIter + 1), Format)
                    rowClassLen += rowAttrLen
                worksheet.merge_range(iterRow - rowClassLen, column + 1, iterRow - 1, column + 1, "Заболевание " + str(classIter + 1), Format)
                worksheet.merge_range(iterRow - rowClassLen, column, iterRow - 1, column, "ИБ " + str(IbIter + 1), Format)
        
        # Ширина колонок
        worksheet.set_column(0, 11, 12)
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(6, 6, 0.75)
        worksheet.set_column(8, 8, 15)

        
        
#a = MBZ(3)
#a.AttributeGeneration()
#a.ClassGeneration(1)
##print(a.classValues)
##print(a.attributePossibleValues)
#a.ToExcel()
#print(a.attributeNormalValues)

import numpy as np
import xlsxwriter as xls
import itertools
import copy

RATIO = 0.20
RATIO_COUNT = 1
# Границы кол-ва ПД
LEFT_CHPD_CONSTANT = 2
RIGHT_CHPD_CONSTANT = 4

# Границы моментов наблюдения
LEFT_MN_CONSTANT = 1 # 
RIGHT_MN_CONSTANT = 2 #

# Границы возможных значений числовых признаков
LEFT_NUM_CONSTANT = 0
RIGHT_NUM_CONSTANT = 80

# Границы кол-ва значений категориальных признаков
LEFT_SIZE_KATEGORIAL_CONSTANT = 2
RIGHT_SIZE_KATEGORIAL_CONSTANT = 10

# Минимальное расстояние между левой и правой границами возможных значений числовых признаков
MINIMUM_LENGTH_NUM = 20


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
    
                ),
            ],
        ],
    ],
]

# mvdTable
[ # <- Классы (Заболевания)
	[ # <- Истории болезней 
		[ # <- Признаки
			[ # <- Момент наблюдения 
				( # <- Значения (МН, значение в МН)
    
                ),
			],
		],
	],
]  

class DataMining:
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
            kategorialSize = np.random.randint(LEFT_SIZE_KATEGORIAL_CONSTANT, RIGHT_SIZE_KATEGORIAL_CONSTANT + 1)
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
        self.classSize = classSize
        self.classValues = []
        for numClass in range(classSize):
            mas = []
            for numAttribute in range(self.attributeSize):
                rest = [0] * np.random.randint(LEFT_CHPD_CONSTANT, RIGHT_CHPD_CONSTANT + 1)
                upAndDownBorder = [0] * len(rest)
                for numPD in range(len(rest)):
                    upAndDownBorder[numPD] = np.random.randint(1, 25, 2) # -----
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
                            if checkDifference and ((self.attributePossibleValues[numAttribute][1] - self.attributePossibleValues[numAttribute][0]) - (thisPD[1] - thisPD[0])) \
                                 / (self.attributePossibleValues[numAttribute][1] - self.attributePossibleValues[numAttribute][0]) > RATIO and \
                                    (self.attributePossibleValues[numAttribute][1] - self.attributePossibleValues[numAttribute][0]) \
                                 % (thisPD[1] - thisPD[0]) > RATIO_COUNT:
                                break
                        rest[numPD] = thisPD
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
        worksheet.set_column(0, 26, 12) # Установка размера колонок

        rowSlov = {}

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
        worksheet.set_column(column + 1, column + 1, 25)
        for row in range(1, self.attributeSize + 1):
            worksheet.write(row, column, "Признак " + str(row), Format)
            if type(self.attributePossibleValues[row - 1]) is tuple:
                left, right = self.attributePossibleValues[row - 1]
                worksheet.write(row, column + 1, '[' + str(int(left)) + '-' + str(int(right)) + ']', Format)
            elif type(self.attributePossibleValues[row - 1]) is list:
                listAttrRow = '{'
                row_len = 15
                for i in range(len(self.attributePossibleValues[row - 1])):
                    listAttrRow += "значение " + str(i + 1) + ", "
                    if (i + 1) % 2 == 0 and i + 1 != len(self.attributePossibleValues[row - 1]):
                        listAttrRow += '\n'
                        row_len += 15
                listAttrRow = listAttrRow[:-2] + '}'
                worksheet.set_row(row, row_len)
                worksheet.write(row, column + 1, listAttrRow, Format)
                rowSlov[row] = row_len
            elif type(self.attributePossibleValues[row - 1]) is int:
                worksheet.write(row, column + 1, "(0, 1)", Format)


        column += 3
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 1, "Нормальные значения (НЗ)", FormatBold)
        worksheet.set_column(column + 1, column + 1, 25)
        for row in range(1, self.attributeSize + 1):
            worksheet.write(row, column, "Признак " + str(row), Format)
            if type(self.attributeNormalValues[row - 1]) is tuple:
                first, second = self.attributeNormalValues[row - 1]
                worksheet.write(row, column + 1, '[' + str(int(first)) + '-' + str(int(second)) + ']', Format)
            elif type(self.attributeNormalValues[row - 1]) is list:
                listAttrRow = '{'
                row_len = 15
                for i in range(len(self.attributeNormalValues[row - 1])):
                    listAttrRow += "значение " + str(i + 1) + ", "
                    if (i + 1) % 2 == 0 and i + 1 != len(self.attributeNormalValues[row - 1]):
                        listAttrRow += '\n'
                        row_len += 15
                listAttrRow = listAttrRow[:-2] + '}'
                worksheet.write(row, column + 1, listAttrRow, Format)
                if row in rowSlov:
                    worksheet.set_row(row, max(row_len, rowSlov[row]))
                    rowSlov[row] = max(row_len, rowSlov[row])
                else:
                    worksheet.set_row(row, row_len)
            elif type(self.attributeNormalValues[row - 1]) is int:
                worksheet.write(row, column + 1, self.attributeNormalValues[row - 1], Format)


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
        
        column += 4
        worksheet.set_column(column - 1, column - 1, 0.75)
        worksheet.merge_range(0, column, 0, column + 3, "Значение для периода (ЗДП)", FormatBold)
        worksheet.set_column(column + 3, column + 3, 25)
        iterRow = 0
        for classIter in range(self.classSize):
            for attrIter in range(self.attributeSize):
                chPD = len(self.classValues[classIter][attrIter][0])
                for PD in range(chPD):
                    row_len = 15
                    worksheet.write(1 + iterRow, column, "Заболевание " + str(classIter + 1), Format)
                    worksheet.write(1 + iterRow, column + 1, "Признак " + str(attrIter + 1), Format)
                    worksheet.write(1 + iterRow, column + 2, PD + 1, Format)
                    if type(self.attributeNormalValues[attrIter]) is tuple:
                        left, right = self.classValues[classIter][attrIter][0][PD]
                        outPutRow = '[' + str(int(left)) + '-' + str(int(right)) + ']'
                    elif type(self.attributeNormalValues[attrIter]) is list:
                        outPutRow = ''
                        for i in range(len(self.classValues[classIter][attrIter][0][PD])):
                            outPutRow += 'значение ' + str(self.classValues[classIter][attrIter][0][PD][i]) + ', ' ####
                            if (i + 1) % 2 == 0 and i + 1 != len(self.classValues[classIter][attrIter][0][PD]):
                                outPutRow += '\n'
                                row_len += 15
                        outPutRow = outPutRow[:-2]
                        if iterRow + 1 in rowSlov:
                            worksheet.set_row(iterRow + 1, max(row_len, rowSlov[iterRow + 1]))
                            rowSlov[iterRow + 1] = max(row_len, rowSlov[iterRow + 1])
                        else:
                            worksheet.set_row(iterRow + 1, row_len)
                    elif type(self.attributeNormalValues[attrIter]) is int:
                        outPutRow = self.classValues[classIter][attrIter][0][PD]
                    worksheet.write(1 + iterRow, column + 3, outPutRow, Format)
                    iterRow += 1
        worksheet.set_column(column, column, 15)

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


        mvdTable = []
        for classIter in range(self.classSize):
            ibMass = []
            for IbIter in range(self.IbSize):
                attrMas = []
                for attrIter in range(self.attributeSize):
                    pdSize = len(self.pdMnValues[classIter][IbIter][attrIter])
                    pdMas = []
                    summatorPD = 0
                    for PD in range(pdSize):
                        durationPD, chMN = self.pdMnValues[classIter][IbIter][attrIter][PD]
                        leftDurationMN, rightDurationNM = 1, durationPD - chMN + 2 # Поменять на + 1, если ВГ не надо касаться НГ
                        for MN in range(chMN):
                            valueInPD = self.classValues[classIter][attrIter][0][PD]
                            if type(valueInPD) is tuple:
                                valueInMN = int(np.random.randint(valueInPD[0], valueInPD[1] + 1))
                            elif type(valueInPD) is list:
                                indexValueKategorial = int(np.random.randint(0, len(valueInPD)))
                                valueInMN = valueInPD[indexValueKategorial]
                            elif type(valueInPD) is int:
                                valueInMN = valueInPD
                            if leftDurationMN < rightDurationNM - 1:
                                mn = int(np.random.randint(leftDurationMN, rightDurationNM))
                            else:
                                mn = leftDurationMN
                            pdMas.append((mn + summatorPD, valueInMN))
                            leftDurationMN, rightDurationNM = mn + 1, rightDurationNM + 1
                        summatorPD += durationPD
                    attrMas.append(pdMas)
                ibMass.append(attrMas)
            mvdTable.append(ibMass)
        self.mvdTable = mvdTable

    
    def ToExcelMVD(self, workbook):
        worksheet = workbook.add_worksheet('МВД')
        Format = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': '#FBD4B4', 'border': 1})
        FormatBold = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': '#FBD4B4', 'border': 1, 'bold': True})
        column = 0
        worksheet.merge_range(0, column, 0, column + 5, "(ИБ, заболевание, признак, номер ПД, длительность ПД, число МН в ПД)", FormatBold)
        iterRow = 1
        historyIter = 1
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
                worksheet.merge_range(iterRow - rowClassLen, column, iterRow - 1, column, "ИБ " + str(historyIter), Format)
                historyIter += 1
        
        column += 7
        iterRow = 1
        worksheet.merge_range(0, column, 0, column + 4, "Выборка данных (ИБ, заболевание, признак, МН, значение в МН)", FormatBold)
        historyIter = 1
        for classIter in range(self.classSize):
            for IbIter in range(self.IbSize):
                rowClassLen = 0
                for attrIter in range(self.attributeSize):
                    rowAttrLen = 0
                    pdSize = len(self.pdMnValues[classIter][IbIter][attrIter])
                    mnIter = 0
                    for PD in range(pdSize):
                        chMN = self.pdMnValues[classIter][IbIter][attrIter][PD][1]
                        rowAttrLen += chMN
                        for MN in range(chMN):
                            valueInPD = self.classValues[classIter][attrIter][0][PD]
                            if type(valueInPD) is tuple:
                                valueInMN = self.mvdTable[classIter][IbIter][attrIter][mnIter][1]
                                worksheet.write(iterRow, column + 4, valueInMN, Format)
                            elif type(valueInPD) is list:
                                worksheet.write(iterRow, column + 4, "значение " + str(self.mvdTable[classIter][IbIter][attrIter][mnIter][1]), Format)
                            elif type(valueInPD) is int:
                                worksheet.write(iterRow, column + 4, valueInPD, Format)
                            mn = self.mvdTable[classIter][IbIter][attrIter][mnIter][0]
                            worksheet.write(iterRow, column + 3, mn, Format)
                            mnIter += 1
                            iterRow += 1
                    if rowAttrLen != 1:
                            worksheet.merge_range(iterRow - rowAttrLen, column + 2, iterRow - 1, column + 2, "Признак " + str(attrIter + 1), Format)
                    else:
                        worksheet.write(iterRow - 1, column + 2, "Признак " + str(attrIter + 1), Format)
                    rowClassLen += rowAttrLen
                worksheet.merge_range(iterRow - rowClassLen, column + 1, iterRow - 1, column + 1, "Заболевание " + str(classIter + 1), Format)
                worksheet.merge_range(iterRow - rowClassLen, column, iterRow - 1, column, "ИБ " + str(historyIter), Format)
                historyIter += 1
        
        # Ширина колонок
        worksheet.set_column(0, 11, 12)
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(6, 6, 0.75)
        worksheet.set_column(8, 8, 15)

    def IfbzBorderDelimiter(self):
        ifbzTableAttr, ifbzTableValue, ifbzTableVGNG  = [], [], []
        for classIter in range(self.classSize):
            ibMass, ibMassValue, ibMassVGNG = [], [], []
            for IbIter in range(self.IbSize):
                attrMass, attrMassValue, attrMassVGNG = [], [], []
                for attrIter in range(self.attributeSize):
                    masPD = self.mvdTable[classIter][IbIter][attrIter]
                    npMasPD = np.array(masPD)
                    masK = [i for i in range(len(masPD))]
                    masProv = npMasPD[:, 1]
                    result, resultValue, resultVGNG = [], [], []
                    for numOfPd in range(1, RIGHT_CHPD_CONSTANT + 1): #for numOfPd in range(1, len(masPD) + 1):
                        pdMass, pdMassValue, pdMassVGNG = [], [], []
                        a = itertools.combinations(masK, numOfPd)

                        counter_a = 0
                        summ_a = 0
                        for i in a:
                            flag = True
                            resOut, resOutValue, resOutVGNG = [], [], []
                            if numOfPd == 1:
                                resOut.append(masPD[-1][0])
                                resOutValue.append(set(masProv))
                                resOutVGNG.append((masPD[-1][0], masPD[-1][0]))
                            elif numOfPd >= 2:
                                gran0 = 0
                                for iterPD in range(1, len(i)):
                                    if iterPD == 1:
                                        left = 0
                                    else:
                                        left = i[iterPD - 1]
                                    
                                    if iterPD == len(i) - 1:
                                        right = len(masPD)
                                    else:
                                        right = i[iterPD + 1]
                                    if iterPD == len(i) - 1:
                                        resOutVGNG.append((npMasPD[i[iterPD] - 1, 0] - gran0, npMasPD[i[iterPD] - 1, 0] - gran0))
                                        gran0 = (npMasPD[i[iterPD] - 1, 0] + npMasPD[i[iterPD], 0]) // 2
                                        resOutVGNG.append((masPD[-1][0] - gran0, masPD[-1][0] - gran0))
                                    else:
                                        resOutVGNG.append((npMasPD[i[iterPD] - 1, 0] - gran0, npMasPD[i[iterPD], 0] - 1 - gran0))
                                    gran0 = (npMasPD[i[iterPD] - 1, 0] + npMasPD[i[iterPD], 0]) // 2
                                    mas_1 = set(masProv[left:i[iterPD]])
                                    mas_2 = set(masProv[i[iterPD]:right])
                                    res = (npMasPD[i[iterPD] - 1, 0], npMasPD[i[iterPD], 0])
                                    resOut.append(res)
                                    resOutValue.append(mas_1)
                                    if iterPD == len(i) - 1:
                                        resOutValue.append(mas_2)
                                    
                                    if not mas_1.isdisjoint(mas_2):
                                        flag = False
                                        break
                            try:
                                flag_2 = resOut not in result
                            except ValueError:
                                flag_2 = True
                                for k in result:
                                    if len(k) != len(resOut):
                                        continue
                                    else:
                                        print(result)
                                        print(resOut)
                                    if type(k[0]) == type(resOut[0]) and k == resOut:
                                        flag_2 = False
                                        break
                            if  flag and flag_2:
                                counter_a += 1
                                if counter_a == 100:
                                    summ_a += 100
                                    print(summ_a, flush=True)
                                    counter_a = 0
                                resultValue.append(resOutValue)
                                result.append(resOut)
                                resultVGNG.append(resOutVGNG)
                        
                        pdMassValue.append(resultValue)
                        pdMass.append(result)
                        pdMassVGNG.append(resultVGNG)
                    attrMassValue.extend(pdMassValue)
                    attrMass.extend(pdMass)
                    attrMassVGNG.extend(pdMassVGNG)
                ibMassValue.append(attrMassValue)
                ibMass.append(attrMass)
                ibMassVGNG.append(attrMassVGNG)
            ifbzTableValue.append(ibMassValue)
            ifbzTableAttr.append(ibMass)
            ifbzTableVGNG.append(ibMassVGNG)
        self.ifbzTableValue = ifbzTableValue
        self.ifbzTableAttr = ifbzTableAttr
        self.ifbzTableVGNG = ifbzTableVGNG

        #for i in range(self.IbSize):
        #    print("--"*20, "Периоды")
        #    print(self.ifbzTableAttr[0][i][0])
        #    print("--"*20, "ЗДП")
        #    print(self.ifbzTableValue[0][i][0])
        #    print("--"*20, "Длительность периода")
        #    print(self.ifbzTableVGNG[0][i][0])
        #    print("--"*20, "Моменты наблюдения")
        #    print(self.mvdTable[0][i][0])
        #    print()

    @staticmethod
    def CheckBorderDelimiterTruth(massOfCheck):
        flag = True
        numOfPd = len(massOfCheck)
        if numOfPd >= 2:
            for iterPD in range(1, len(massOfCheck)):
                mas_1 = massOfCheck[iterPD - 1]
                mas_2 = massOfCheck[iterPD]
                if not mas_1.isdisjoint(mas_2):
                    flag = False
                    break
        return flag

    def IfbzBorderSummator(self):
        classMass = []
        classMassVGNG = []
        print("Начало генерации", flush=True)
        for classIter in range(self.classSize):
            print(classIter + 1, "класс", flush=True)
            attrMas = []
            attrMasVGNG = []
            for attrIter in range(self.attributeSize): #(1, 2)
                print(attrIter + 1, "признак", flush=True)
                attrUnion = []
                attrUnionVGNG = []
                for IbIter in range(0, self.IbSize): # Как вариант можно для ПД = 1 провести операцию вне цикла PdNum, просто объединив границы и значения множеств
                                                  # а для ПД > 1 сделать проверку на получившиеся объединённые множества, пропустив их через новую функцию
                                                  # проверки таковых, но для этого нужно вынести её из функции ifbzBorderDelimiter
                                                  #
                                                  # Есть ещё один вариант - Это внаглую объеденить все множества по их номеру ИБ и уже потом, в отдельном цикле
                                                  # проверить на правильность объединения (но тогда массивы раздуются из-за того что некоторые ИБ имеют по
                                                  # несколько ЧПД одинакового размера)
                    print(IbIter + 1, "история болезни", flush=True)
                    testMas = {i: [] for i in range(1, len(self.ifbzTableValue[classIter][IbIter][attrIter][-1]) + 1)}
                    testMasVGNG = {i: [] for i in range(1, len(self.ifbzTableValue[classIter][IbIter][attrIter][-1]) + 1)}
                    for PdNum in range(len(self.ifbzTableValue[classIter][IbIter][attrIter])):
                        testMas[len(self.ifbzTableValue[classIter][IbIter][attrIter][PdNum])].append(self.ifbzTableValue[classIter][IbIter][attrIter][PdNum])
                        testMasVGNG[len(self.ifbzTableValue[classIter][IbIter][attrIter][PdNum])].append(self.ifbzTableVGNG[classIter][IbIter][attrIter][PdNum])
                    if IbIter == 0:
                        attrUnion = testMas
                        attrUnionVGNG = testMasVGNG
                    else:
                        for PdNum in range(1, min(len(attrUnion), len(testMas)) + 1):
                            print(PdNum + 1, "период динамики", flush=True)
                            if len(attrUnion[PdNum]) == 0 or len(testMas[PdNum]) == 0:
                                continue
                            zatychkaMas = []
                            zatychkaMasVGNG = []
                            counter_i = 0
                            for i in range(len(attrUnion[PdNum])):
                                if counter_i == 100:
                                    print(i + 1, "из", len(attrUnion[PdNum]), "Признак", attrIter, flush=True)
                                    counter_i = 0
                                counter_i += 1
                                for j in range(len(testMas[PdNum])):
                                    zatychkaMas_2 = copy.deepcopy(attrUnion[PdNum][i]) ###
                                    zatychkaMas_2VGNG = copy.deepcopy(attrUnionVGNG[PdNum][i])
                                    for iterKar in range(PdNum):
                                        zatychkaMas_2[iterKar].update(testMas[PdNum][j][iterKar])
                                        zatychkaMas_2VGNG[iterKar] = (max(zatychkaMas_2VGNG[iterKar][0], testMasVGNG[PdNum][j][iterKar][0]), \
                                                                      min(zatychkaMas_2VGNG[iterKar][1], testMasVGNG[PdNum][j][iterKar][1]))
                                    # Здесь нужна проверка на не пересечение элементов
                                    # И если всё хорошо - добавление
                                    if self.CheckBorderDelimiterTruth(zatychkaMas_2):
                                        zatychkaMas.append(zatychkaMas_2)
                                        zatychkaMasVGNG.append(zatychkaMas_2VGNG)
                            attrUnion[PdNum] = zatychkaMas
                            attrUnionVGNG[PdNum] = zatychkaMasVGNG
                attrMas.append(attrUnion)
                attrMasVGNG.append(attrUnionVGNG)
            classMass.append(attrMas)
            classMassVGNG.append(attrMasVGNG)
        self.IfbzSet = classMass
        self.IfbzVGNG = classMassVGNG

    def ToExcelIFBZ(self, workbook):
        worksheet = workbook.add_worksheet('ИФБЗ')
        Format = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': '#FBD4B4', 'border': 1})
        FormatBold = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': '#FBD4B4', 'border': 1, 'bold': True})
        FormatPartition = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': 'red', 'border': 1, 'bold': True})
        FormatPartitionGray = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': 'gray', 'border': 1, 'bold': True})
        FormatPartitionYellow = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': 'yellow', 'border': 1, 'bold': True})
        column = 0
        iterRow = 0
        for classIter in range(self.classSize):
            for attrIter in range(self.attributeSize):
                worksheet.set_column(column, column + 2, 15)
                worksheet.write(0, column, "Заболевание " + str(classIter + 1), Format)
                worksheet.write(0, column + 1, "Признак " + str(attrIter + 1), Format)
                iterRow += 1
                for IBiter in range(self.IbSize):
                    rowAttrLen = 0
                    pdSize = len(self.pdMnValues[classIter][IBiter][attrIter])
                    mnIter = 0
                    for PD in range(pdSize):
                        chMN = self.pdMnValues[classIter][IBiter][attrIter][PD][1]
                        rowAttrLen += chMN
                        for MN in range(chMN):
                            valueInPD = self.classValues[classIter][attrIter][0][PD]
                            if type(valueInPD) is tuple:
                                valueInMN = self.mvdTable[classIter][IBiter][attrIter][mnIter][1]
                                worksheet.write(iterRow, column + 2, valueInMN, Format)
                            elif type(valueInPD) is list:
                                worksheet.write(iterRow, column + 2, "значение " + str(self.mvdTable[classIter][IBiter][attrIter][mnIter][1]), Format)
                            elif type(valueInPD) is int:
                                worksheet.write(iterRow, column + 2, valueInPD, Format)
                            mn = self.mvdTable[classIter][IBiter][attrIter][mnIter][0]
                            worksheet.write(iterRow, column + 1, mn, Format)
                            mnIter += 1
                            iterRow += 1
                    if rowAttrLen != 1:
                            worksheet.merge_range(iterRow - rowAttrLen, column, iterRow - 1, column, "ИБ " + str(IBiter + 1), Format)
                    else:
                        worksheet.write(iterRow - 1, column, "ИБ " + str(IBiter + 1), Format)

                iterRow = 0
                column += 4
                maxIbIter = 0
                for IBiter in range(len(self.ifbzTableAttr[classIter])):
                    worksheet.write(iterRow, column, "ИБ " + str(IBiter + 1), Format)
                    worksheet.write(iterRow, column + 1, "ЧПД 1", FormatBold)
                    worksheet.write(iterRow, column + 2, int(self.ifbzTableAttr[classIter][IBiter][attrIter][0][0]), Format)
                    iterRow += 1
                    ibRowIter = 0
                    #
                    predLen = len(self.ifbzTableAttr[classIter][IBiter][attrIter][1])
                    counterPdLen = 0
                    for itr in range(1, len(self.ifbzTableAttr[classIter][IBiter][attrIter])):
                        if len(self.ifbzTableAttr[classIter][IBiter][attrIter][itr]) != predLen:
                            if counterPdLen != 1:
                                worksheet.merge_range(iterRow - counterPdLen, column + 1, iterRow - 1, column + 1, "ЧПД " + str(predLen + 1), FormatBold)
                            else:
                                worksheet.write(iterRow - 1, column + 1, "ЧПД " + str(predLen + 1), FormatBold)
                            predLen = len(self.ifbzTableAttr[classIter][IBiter][attrIter][itr])
                            maxIbIter = max(maxIbIter, predLen + 1)
                            counterPdLen = 0
                        counterPdLen += 1
                        column_iter = column + 2
                        for itr_PD in range(0, len(self.ifbzTableAttr[classIter][IBiter][attrIter][itr])):
                            result = self.ifbzTableAttr[classIter][IBiter][attrIter][itr][itr_PD]
                            worksheet.write(iterRow, column_iter, "[" + str(result[0]) + "," + str(result[1]) + ")", Format) #--------------- Вот здесь остановился
                            column_iter += 1
                        worksheet.write(iterRow, column_iter, int(self.ifbzTableAttr[classIter][IBiter][attrIter][0][0]), Format)
                        ibRowIter += 1
                        iterRow += 1
                    if counterPdLen != 1:
                        worksheet.merge_range(iterRow - counterPdLen, column + 1, iterRow - 1, column + 1, "ЧПД " + str(predLen + 1), FormatBold)
                    else:
                        worksheet.write(iterRow - 1, column + 1, "ЧПД " + str(predLen + 1), FormatBold)
                    maxIbIter = max(maxIbIter, predLen + 1)
                    worksheet.merge_range(iterRow - ibRowIter - 1, column, iterRow - 1, column, "ИБ " + str(IBiter + 1), FormatBold)
                iterRow = 0
                column += maxIbIter + 3

                iterIfbzSet = self.IfbzSet[classIter][attrIter]
                iterIfbzVGNG = self.IfbzVGNG[classIter][attrIter]
                worksheet.write(iterRow, column, "ЧПД", Format)
                worksheet.write(iterRow, column + 1, "ПД", Format)
                worksheet.write(iterRow, column + 2, "Значения", Format)
                worksheet.write(iterRow, column + 3, "ВГ", Format)
                worksheet.write(iterRow, column + 4, "НГ", Format)
                iterRow += 1
                flag = True
                
                for PD in range(1, len(iterIfbzSet) + 1):
                    if PD != 1 and flag:
                        worksheet.merge_range(iterRow, column, iterRow, column + 4, "", FormatPartitionGray)
                        flag = False
                        iterRow += 1
                    for variant in range(len(iterIfbzSet[PD])):
                        flag = True
                        if variant != 0:
                            worksheet.merge_range(iterRow, column, iterRow, column + 4, "", FormatPartition)
                            iterRow += 1
                        worksheet.write(iterRow, column, "ЧПД " + str(PD), Format)
                        variantCounter = iterRow
                        for PDiter in range(len(iterIfbzSet[PD][variant])):
                            worksheet.write(iterRow, column + 1, PDiter + 1, Format)
                            ##
                            if type(self.attributeNormalValues[attrIter]) is tuple:
                                resOut = ', '.join(map(str, list(iterIfbzSet[PD][variant][PDiter])))
                            elif type(self.attributeNormalValues[attrIter]) is list:
                                resOut = ''
                                masIfbz = list(iterIfbzSet[PD][variant][PDiter])
                                for i in range(len(masIfbz)):
                                    resOut += 'значение ' + str(masIfbz[i]) + ', ' ####
                                resOut = resOut[:-2]
                            elif type(self.attributeNormalValues[attrIter]) is int:
                                resOut = self.classValues[classIter][attrIter][0][PDiter]
            
                            worksheet.write(iterRow, column + 2, resOut, Format)
                            worksheet.write(iterRow, column + 3, iterIfbzVGNG[PD][variant][PDiter][0], Format)
                            worksheet.write(iterRow, column + 4, iterIfbzVGNG[PD][variant][PDiter][1], Format)
                            iterRow += 1
                        worksheet.merge_range(variantCounter, column, iterRow - 1, column, "ЧПД " + str(PD), Format) 
                iterRow = 0
                column += 8

                ##################
                worksheet.set_column(column - 2, column - 2, 0.5)
                worksheet.set_column(column - 6, column - 6, 25)
                worksheet.merge_range(0, column - 2, 1000, column - 2, "", FormatPartitionYellow)


    def ToExcelMBZvsIFBZ(self, workbook):
        worksheet = workbook.add_worksheet('МБЗ vs ИФБЗ')
        Format = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': '#FBD4B4', 'border': 1})
        FormatBold = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': '#FBD4B4', 'border': 1, 'bold': True})
        FormatPartition = workbook.add_format({'align': 'center', 'valign': 'top', 'bg_color': 'red', 'border': 1, 'bold': True})
        column = 0
        worksheet.write(0, column, "Заболевание", Format)
        worksheet.write(0, column + 1, "Признак", Format)
        worksheet.write(0, column + 2, "Количество правильных ЧПД", Format)
        worksheet.write(0, column + 3, "ЧПД", Format)
        worksheet.write(0, column + 4, "ПД", Format)
        worksheet.write(0, column + 5, "ЗДП МБЗ", Format)
        worksheet.write(0, column + 6, "ЗДП ИФБЗ", Format)
        worksheet.write(0, column + 7, "%", Format)
        worksheet.write(0, column + 8, "НГ", Format)
        worksheet.write(0, column + 9, "ВГ", Format)
        iterRow = 1
        for classIter in range(self.classSize):
            worksheet.write(iterRow, column, "Заболевание " + str(classIter + 1), Format)
            rowClassCounter = 0
            for attrIter in range(self.attributeSize):
                counterAllVariant = 0
                chPD = len(self.classValues[classIter][attrIter][0])
                worksheet.write(iterRow, column + 1, "Признак " + str(attrIter + 1), Format)

                worksheet.write(iterRow, column + 3, chPD, Format)
                rowAttrCounter = 0
                PDnum = chPD - 1
                if len(self.IfbzSet[classIter][attrIter][PDnum + 1]) == 0:
                    continue
                
                for PD in range(1, chPD + 1):
                    counterAllVariant += len(self.IfbzSet[classIter][attrIter][PD])
                counterTrueVariant = len(self.IfbzSet[classIter][attrIter][chPD])
                for variant in range(len(self.IfbzSet[classIter][attrIter][PDnum + 1])):
                    if variant != 0:
                        worksheet.merge_range(iterRow, column + 4, iterRow, column + 9, "", FormatPartition)
                        iterRow += 1
                        rowAttrCounter += 1
                        
                    for PDiter in range(0, PDnum + 1):
                        worksheet.write(iterRow, column + 4, PDiter + 1, Format)
                        
                        if type(self.attributeNormalValues[attrIter]) is tuple:
                            left, right = self.classValues[classIter][attrIter][0][PDiter]
                            outPutRow = '[' + str(int(left)) + '-' + str(int(right)) + ']'
                        elif type(self.attributeNormalValues[attrIter]) is list:
                            outPutRow = ''
                            for i in range(len(self.classValues[classIter][attrIter][0][PDiter])):
                                outPutRow += 'значение ' + str(self.classValues[classIter][attrIter][0][PDiter][i]) + ', ' ####
                            outPutRow = outPutRow[:-2]
                        elif type(self.attributeNormalValues[attrIter]) is int:
                            outPutRow = self.classValues[classIter][attrIter][0][PDiter]
                        worksheet.write(iterRow, column + 5, outPutRow, Format)
                        ng_mbz, vg_mbz = self.classValues[classIter][attrIter][1][PDiter]
                        vg_ifbz, ng_ifbz = self.IfbzVGNG[classIter][attrIter][PDnum + 1][variant][PDiter]
                        worksheet.write(iterRow, column + 8, ng_mbz - ng_ifbz, Format)
                        worksheet.write(iterRow, column + 9, vg_mbz - vg_ifbz, Format)
                        if type(self.attributeNormalValues[attrIter]) is tuple:
                            lstOut = list(self.IfbzSet[classIter][attrIter][PDnum + 1][variant][PDiter])
                            outPutRow = ', '.join(map(str, lstOut))
                            outPutRowCounterMask = np.sum(np.logical_and(left <= np.array(lstOut, int), np.array(lstOut, int) <= right)) * 100 // (right - left + 1)
                        elif type(self.attributeNormalValues[attrIter]) is list:
                            outPut = list(self.IfbzSet[classIter][attrIter][PDnum + 1][variant][PDiter])
                            outPutRow = ""
                            outPutRowCounterMask = len(list(set(self.classValues[classIter][attrIter][0][PDiter]).intersection(self.IfbzSet[classIter][attrIter][PDnum + 1][variant][PDiter]))) * 100
                            outPutRowCounterMask //= len(self.classValues[classIter][attrIter][0][PDiter])

                            for key in outPut:
                                outPutRow += "значение" + str(key) + ", "
                            outPutRow = outPutRow[:-2]
                        else:
                            outPutRow = list(self.IfbzSet[classIter][attrIter][PDnum + 1][variant][PDiter])[0]
                            if list(self.IfbzSet[classIter][attrIter][PDnum + 1][variant][PDiter])[0] == self.classValues[classIter][attrIter][0][PDiter]:
                                outPutRowCounterMask = 100
                            else:
                                outPutRowCounterMask = 0
                        worksheet.write(iterRow, column + 6, outPutRow, Format)

                        worksheet.write(iterRow, column + 7, outPutRowCounterMask, Format)
                        iterRow += 1
                        rowAttrCounter += 1
                rowClassCounter += rowAttrCounter
                worksheet.merge_range(iterRow - rowAttrCounter, column + 1, iterRow - 1, column + 1, "Признак " + str(attrIter + 1), FormatBold)
                worksheet.merge_range(iterRow - rowAttrCounter, column + 3, iterRow - 1, column + 3, chPD, FormatBold)
                worksheet.merge_range(iterRow - rowAttrCounter, column + 2, iterRow - 1, column + 2, str(counterTrueVariant) + "|" + str(counterAllVariant), FormatBold)

            worksheet.merge_range(iterRow - rowClassCounter, column, iterRow - 1, column, "Заболевание " + str(classIter + 1), FormatBold)


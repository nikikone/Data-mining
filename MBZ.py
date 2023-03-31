SIZE_KATEGORIAL_CONSTANT = 10
LEFT_NUM_CONSTANT = 0
RIGHT_NUM_CONSTANT = 1000
LEFT_CHPD_CONSTANT = 1
RIGHT_CHPD_CONSTANT = 5
import numpy as np

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
                for numPD in range(len(rest)):
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
                mas.append(rest)
            self.classValues.append(mas)
        
a = MBZ(3)
a.AttributeGeneration()
a.ClassGeneration(2)
print(a.classValues)
print(a.attributePossibleValues)
#print(a.attributeNormalValues)


SIZE_KATEGORIAL_CONSTANT = 10
LEFT_NUM_CONSTANT = 0
RIGHT_NUM_CONSTANT = 1000

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
        self.attribute = []
        for _ in range(numSize):
            self.attribute.append(np.random.randint(LEFT_NUM_CONSTANT, RIGHT_NUM_CONSTANT + 1, 2))
        
        for _ in range(katSize):
            kategorialSize = np.random.randint(2, SIZE_KATEGORIAL_CONSTANT + 1)
            kategorial = []    
            for i in range(1, kategorialSize):
                kategorial.append('Значение' + str(i))
            self.attribute.append(kategorial)
        
        for _ in range(binSize):
            self.attribute.append(1)
        #self.attribute = np.array(self.attribute)
        
a = MBZ(2)
a.AttributeGeneration()
print(a.attribute)
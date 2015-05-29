#dbFeature is the package for data files' I/O
import struct as st
import copy as cp

class dbFeature:
    def __init__(self):
        self.nNum = 0
        self.nDim = 0
        self.pData = 0

    def set_data(self,pData, nNum, nDim):
        assert(type(pData) == list)
        assert(len(pData) == nNum*nDim)
        self.pData = cp.copy(pData)
        self.nNum = nNum
        self.nDim = nDim

    def set_size(self, nNum, nDim):
        self.nNum = nNum
        self.nDim = nDim

    def get_number(self):
        return self.nNum

    def get_dim(self):
        return self.nDim

    def get_data(self, begin=0, end=1):
        #get data of [begin,end)
        return self.pData[begin*self.nDim : end*self.nDim]

    def save_to_text_file(self, filename):
        outFile = open(filename,'w')
        outFile.write(str(self.nNum)+'\n')
        outFile.write(str(self.nDim)+'\n')
        num = 0
        for i in xrange(self.nNum):
            for j in xrange(self.nDim):
                outFile.write(str(self.pData[num]) + ' ')
                num += 1
            outFile.write('\n')
        outFile.close()

    def read_from_text_file(self, filename, dataType):
        #dataType is  a string  that descripts data type
        #'int' for int
        #'float' for 4 byte float
        #'double' for 8 byte float

        assert(dataType=='int' or dataType=='float' or dataType=='double')
        T = int
        if(dataType == 'float' or dataType=='double'): T = float
        inFile = open(filename,'r')
        self.nNum = int(inFile.readline())
        self.nDim = int(inFile.readline())
        self.pData = []
        for i in xrange(self.nNum):
            record = inFile.readline().strip().split()
            self.pData += [T(item) for item in record]
        print self.pData
        inFile.close()

    def save_to_file(self, filename):
        #open support int and float
        T = 'i'
        if(type(self.pData[0])==float): T = 'f'

        outFile = open(filename,'wb')
        outFile.write(st.pack('ii',self.nNum,self.nDim))
        for item in self.pData:
            outFile.write(st.pack(T,item))
        outFile.close()

    def read_from_file(self,filename,dataType):
        #dataType is  a string  that descripts data type
        #'int' for int
        #'float' for 4 byte float
        #'double' for 8 byte float
        assert(dataType=='int' or dataType=='float' or dataType=='double')
        T = dataType[0]
        size = 4
        if T == 'd': size = 8

        inFile = open(filename,'rb')
        (self.nNum,self.nDim) = st.unpack('ii', inFile.read(8))
        self.pData = []
        for i in xrange(self.nNum * self.nDim):
            self.pData.append(st.unpack(T,inFile.read(size))[0])
        inFile.close()

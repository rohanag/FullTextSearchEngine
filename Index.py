import sys
from os import getcwd
sys.path.append(getcwd() + '/API')

from IndexAPI import invertedListAppend, writeIndexToFile, MakeIndex, storeMetadata
from time import time
from os import stat, listdir
        
if __name__ == '__main__':
    
    IndexFileName = 'ra2616Index'
    if len(sys.argv) != 2:
        print "Incorrect Number of Arguments to Index, please specify the index location as the only argument..."
        exit()
        
    path = sys.argv[1]
    timeStart = time()
    #Making the index for files in path, stored in InvertedIndex
    InvertedIndex = MakeIndex(path)
    timeEnd = time()   
    writeIndexToFile(IndexFileName, InvertedIndex)
    timeWrite = time()
    storeMetadata(path,'ra2616Metadata')
    print 'Time to make index = ',timeEnd - timeStart, ' seconds'
    print 'Time to make index and write to file = ',timeWrite - timeStart, ' seconds'
    print 'Size of Index (After stemming) = ',stat(IndexFileName).st_size/1024, ' KBytes'
    print 'Number of Unique Words (After stemming) = ', len(InvertedIndex)
    print 'Number of Documents = ',len([f for f in listdir(path)])



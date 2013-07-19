'''
Contains methods related to creation and storage of Inverted Index as well as storage of metadata
'''
from __future__ import division

from json import dump
from os import listdir
from os.path import exists
from Document import parseXML, tokenize, lowercase, filterData, printDocument, getMetadata, stemmer


'''
append words in doc to inverted list 'InvertedIndex'
'''
def invertedListAppend( words, doc, InvertedIndex ):
    doc = int(doc[-4:])
    for pos,w in enumerate(words):
        if w != '':
            if w in InvertedIndex:
                if doc in InvertedIndex[w]:
                    InvertedIndex[w][doc].append(pos)
                else:
                    InvertedIndex[w][doc]= [pos]
            else:
                InvertedIndex[w]={}
                InvertedIndex[w][doc] = [pos]
    return InvertedIndex
    
'''
Writing the index to a file    
'''
def writeIndexToFile(fileName, InvertedIndex):
    with open(fileName, 'wb') as fp:
        dump(InvertedIndex, fp, separators=(',',':'))

'''
calls all functions required to make the index
First reads data from XML files, converts to lowercase, tokenizes data, filters the data (remove empty string), then add words to index        
'''
def MakeIndex(path):
    InvertedIndex = {}
    InvertedIndex['path_of_documents'] = path
    if exists(path):
        textFiles = [f for f in listdir(path)]
    else:
        print path,'is not a valid path, exiting...'
        exit()
    for file in textFiles:
        text = parseXML( path + "/" + file )
        text = lowercase(text)
        text = tokenize(text)
        text = filterData(text)
        text = stemmer(text)
        InvertedIndex = invertedListAppend( text, file, InvertedIndex )    
    return InvertedIndex
'''
storing the metadata of all files in the index in fileName    
'''
def storeMetadata(path,fileName):
    if exists(path):
        textFiles = [f for f in listdir(path)]
    else:
        print path,'is not a valid path, exiting...'
        exit()
    metaData = {}
    for file in textFiles:
        metaData[file] = getMetadata( path + "/" + file )
    with open(fileName, 'wb') as fp:
        dump(metaData, fp, separators=(',',':'))    

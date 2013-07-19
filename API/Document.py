'''
#Porter stemmer taken from http://tartarus.org/martin/PorterStemmer/index-old.html

Contains methods related to reading from documents, processing data before indexing, and getting document snippet from data
'''

import xml.etree.cElementTree as ElementTree
import porter
from string import zfill
from os.path import isfile
import re

    
    
'''
parses the file given in fileName, returns text in string
'''
def parseXML(filename):
    if isfile(filename):
        tree = ElementTree.parse(filename)
    else:
	print ''
        print filename,'is not a valid file.'
	print ''
        return ' '
    text= ' '
    for child in tree.getroot():
        if child.tag not in ('DOCNO','BIBLIO'): 
            text += child.text
    return text

'''
returns the meta data of the fileName in a dictionary, keys are xml tags 'DOCNO','BIBLIO','AUTHOR'
'''
def getMetadata(filename):
    if isfile(filename):
        tree = ElementTree.parse(filename)
    else:
        print filename,'is not a valid file. Program terminating...'
        exit()
    meta = {}
    for child in tree.getroot():
        if child.tag in ('DOCNO','BIBLIO','AUTHOR'): 
            meta[child.tag] = child.text
    return meta
    
'''
returns stemmed version of words in word    
'''
def stemmer(word):
    stemObj = porter.PorterStemmer()
    return [stemObj.stem(w,0,len(w)-1) for w in word]

'''
Tokenizes the string        
'''
def tokenize(string):
    return re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",string)
    
'''
Converts string to lowercase
'''
def lowercase(string):
    return string.lower()

'''
prevents periods , commas from getting inserted in the index    
'''
def filterData(wordList):
    return [word for word in wordList if word not in [".",","] ]
    
'''
given a document name, prints the document. If title = True, prints only the title of the document
'''
def printDocument(file, title = False):
    if isfile(file):
        tree = ElementTree.parse(file)
    else:
        print ''
        print file,'is not a valid file........'
        print ''
        return
    for child in tree.getroot():
        if title == True and child.tag == 'TITLE':
            print child.text
        elif title == False:
            print child.tag
            print child.text                

'''
finds the number of occurences of searchFor in searchIn
'''
def matches(searchFor,searchIn):
    count = 0
    for words in searchFor:
        count += searchIn.count(words) * (words.count(' ') + 1)
    return count

'''
get snippets of text from documents of length 30 that contain the most number of search query terms
'''
def getSnippets(topDocs, InvIndex, searchFor):
    path = InvIndex['path_of_documents']
    for i,temp in enumerate(searchFor):
        if searchFor[i][0] == '(':
            searchFor[i] = searchFor[i][1:-1]  
    snippets = []
    for docs,pos in topDocs:
        file = path
        file += '/' + 'cranfield' + zfill(str(docs),4)
        text = filterData(tokenize(lowercase(parseXML(file))))
        maxscore = -1
        maxindex = 0
        snippetLength = 30
        for i in range(len(text)-snippetLength):
            score = matches( searchFor, ' '.join(text[i:i+snippetLength]) )
            maxscore = max(score, maxscore)
            if score == maxscore:
                maxindex = i
        snippets.append( ' '.join(text[maxindex:maxindex+snippetLength]) )
    return snippets

'''
prints the contents of the file
'''
def printDoc(docs, path):
    print '----------------------------------------------------------------------------'
    print 'Contents of ',docs
    print '----------------------------------------------------------------------------'
    printDocument(path + '/' + 'cranfield' + zfill(str(docs),4))    
    print '----------------------------------------------------------------------------'
    
'''
prints the Title of docs stored in path
'''
def printTitle(docs, path):
    print '----------------------------------------------------------------------------'
    print 'Title of ',docs
    print '----------------------------------------------------------------------------'    
    printDocument( path + '/' + 'cranfield' + zfill(str(docs),4) , True)    
    print '----------------------------------------------------------------------------'
    

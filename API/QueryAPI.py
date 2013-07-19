'''
Contains methods required for processing the query, sorting the results dictionary recieved from Document.py and printing final results
'''
from __future__ import division

from json import load
from sexpr import SExprTokenizer
from operator import itemgetter
from string import zfill

'''        
Flatten a nested list: e.g. [a,b,[c,d]] => [a,b,c,d]
Function flatten() taken from http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
'''
def flatten(TheList):
    listIsNested = True
    while listIsNested:                
        keepChecking = False
        Temp = []
        for element in TheList:        
            if isinstance(element,list):
                Temp.extend(element)
                keepChecking = True
            else:
                Temp.append(element)
        listIsNested = keepChecking
        TheList = Temp[:]
    return TheList
     
'''
split search string into seperate words, phrases
E.g. 'the "best thing"' => ['the','(best thing)']
'''
def parseSearchString(searchString):
    cnt = searchString.count('"')
    searchString = searchString.strip()
    if cnt%2 == 1:
        print 'Please balance the number of quotes in the Search string... program terminating...'
        exit()
    while cnt:
        cnt -= 2
        searchString = searchString.replace('"','(',1)
        searchString = searchString.replace('"',')',1)
    resultTemp = SExprTokenizer(strict=False).tokenize(searchString)
    #Since nltk doesnt do the best job of tokenizing, im running split on unsplit strings
    result = [x.split() if x[0] != '(' else x for x in resultTemp]
    result = flatten(result)
    while ("!" in result):
        i = result.index("!")
        result[i+1] = "!" + result[i+1]
        result.pop(i)
    return result

'''
Sort a dictionary by value and return sorted list        
'''
def sortByValue(x):
    return sorted( x.iteritems(), key = itemgetter(1), reverse = True )

'''
print documents returned by search and the snippets
'''
def printResults(top5, snippets, round):
    for i, docs in enumerate(top5):
        print str(round*5 + i + 1) + '.) cranfield' + zfill(str(docs[0]),4)
        print ''
        print '...' + snippets[i] + '...'
        print ''
        print '------------------------------------------------------------------------'

'''
Preprocessing includes reading Invertedindex to dictionary 'InvIndex', and making a set of words 'wordset' and documents 'docset'
'''
def preprocess():
    with open('ra2616Index', 'rb') as fp:
        InvIndex = load(fp)
           
    wordSet = set(InvIndex.keys())
    docSet = set(docs for words in InvIndex for docs in InvIndex[words])
    docSet = list(docSet)
    return wordSet, docSet, InvIndex

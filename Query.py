import sys
from os import getcwd
sys.path.append(getcwd() + '/API')
from QueryAPI import parseSearchString, sortByValue, printResults, preprocess
from time import time
from Retreival import searchBoolean, tf, df, freq, similar
from Document import lowercase, tokenize, filterData, printDocument, getSnippets, printDoc, printTitle, stemmer

    
if __name__ == '__main__':
    #wordset is the set of all unique words in index, docset is the set of all documents, invl is the inverted list
    wordSet,docSet,invl = preprocess()
    while True:
        print 'Enter search string: (Empty string to exit)'        
        searchString = raw_input()
        searchString = searchString.strip()
                
        if searchString == '':
            break
        #seperate the individual words or phrases in the searchString
        parsedSearch = parseSearchString(searchString)    
        parsedSearch = stemmer(parsedSearch)
        searchString = ' '.join(parsedSearch)
        #Checking for the type of query desired by the user
        if parsedSearch[0] == 'df':
            print ''
            print 'Document Frequency of \'',searchString[3:],'\' is', df(searchString[3:], wordSet, docSet, invl)
            print ''
            continue
        elif parsedSearch[0] == 'tf':
            newSearch = ' '.join(parsedSearch[2:])
            if len(parsedSearch) == 1:
                print ''
                print 'Please name of document after tf.....'
                print ''
                continue
            print ''
            print 'Term Frequency of \'',newSearch,'\' in Document \'',parsedSearch[1],'\' is', tf(parsedSearch[1], newSearch, wordSet, docSet, invl)
            print ''
            continue
        elif parsedSearch[0] == 'freq':
            print ''
            print 'Frequency of \'',searchString[5:],'\' is', freq(searchString[5:], wordSet, docSet, invl)
            print ''
            continue      
        elif parsedSearch[0] == 'doc':
            print ''
            printDoc(searchString[4:],invl['path_of_documents'])
            print ''
            continue  
        elif parsedSearch[0] == 'titl':
            print ''
            printTitle(searchString[5:],invl['path_of_documents'])
            print ''
            continue   
        elif parsedSearch[0] == 'similar':
            print ''
            similar(docSet, invl, searchString[8:])
            print ''
            continue                      
        timeStart =  time()
        #searchBoolean does the actual searching
        result = searchBoolean(parsedSearch, wordSet, docSet, invl)
        print ''
        print 'Searching took',(time() - timeStart)*1000,'miliseconds'
        print ''
        print len(result), 'Search Results'
        print ''
        sortedResult = sortByValue(result)
        round = 0
        #Displaying sorted results, 5 documents at a time
        while sortedResult:  
            if len(sortedResult) >= 5:
                top5 = sortedResult[:5]
                sortedResult = sortedResult[5:]
            else:
                top5 = sortedResult
                sortedResult = []
            snippets = getSnippets(top5, invl, parsedSearch)
            printResults(top5, snippets, round)
            round += 1
            if sortedResult:
                print ''
                print 'Show next 5 results ? (Enter n to stop): '
                choice = raw_input()
                print ''
                if choice == 'n':
                    break
                    

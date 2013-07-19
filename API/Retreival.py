'''
    Contains methods related to retreival of search results, calculation of best documents for given query, 
    calulation of tf, df, freq, similar words.
'''
from Document import parseXML, tokenize, lowercase, filterData, printDocument, getMetadata, stemmer
from string import zfill

'''
performs the main boolean search function, for terms in searchTerms. Returns a dictionary whose key is documentID, value is score
'''
def searchBoolean(searchTerms, wordSet, docSet, InvIndex):
    result = {}
    notResults = []
    if searchTerms == ['']:
        return
    for terms in searchTerms:
        neg = 0
        phrase = 0
        if terms[0] == "!":
            neg = 1
            terms = terms[1:]
        if terms[0] == "(":
            phrase = 1
            terms = terms[1:-1]
        if phrase == 1:
            tempResult1 = phraseSearch(terms, wordSet, docSet, InvIndex)
        else:
            tempResult1 = getIndex(terms, InvIndex)
        if neg == 1:
            tempResult1 = getNegIndex(tempResult1.keys(), docSet)
            notResults.extend(tempResult1)
        else:
            result = simpleMerge(tempResult1, result)
    if notResults == []:
        return result
    notResults = set(notResults)
    if result == {}:
	for docs in notResults:
	    result[docs] = 1
    return {r:result[r] for r in result if r in notResults}
    
    
'''
Search phrases, returns dictionary {docId : freq of Phrase in docId}
'''
def phraseSearch(phrase, wordSet, docSet, InvIndex):
    words = phrase.strip().strip('"').split()
    words = stemmer(words)
    phraseLen = len(words)
    if not set(words).issubset(wordSet):
        return {}
    if len(words) == 0:
        return {}
    word1 = words[0]
    words.remove(word1)
    mergeList1 = InvIndex[word1]
    while(words):
        word2 = words[0]
        words.remove(word2)
        mergeList2 = InvIndex[word2]
        mergeList1 = phraseMerge(mergeList1, mergeList2)
    for keys, values in mergeList1.items():
        mergeList1[keys] = phraseLen * len(values)
    return mergeList1
    
'''
merges two lists, list1 and list2 and returns merged list. Merged list contains documents which contain words from 
list1 and 2 next to each other.
'''
def phraseMerge(list1, list2):
    list3 = {}
    for docs, positions in list1.items():
        if docs in list2:
            positions3 = []
            positions2 = list2[docs]
            for pos in positions:
                if pos + 1 in positions2:
                    positions3.append(pos+1)
            if positions3 != []:
                list3[docs] = positions3
    return list3    
    
'''
merges list1 and list2, combining scores for each document in the list. Equivalend to fuzzy OR. Returns the merged dcitionary.
returns dictionary{docId: score of DocID}
'''
def simpleMerge(list1, list2):
    list3 = {}
    for docs in list1.keys():
        if docs in list2:
            list3[docs] = list2[docs] + list1[docs]
        else:
            list3[docs] = list1[docs]
    for docs in list2.keys():
        if docs not in list1:
            list3[docs] = list2[docs]
    return list3

'''
get index listing for word in InvIndex
'''
def getIndex(word, InvIndex):
    result = {}
    if word not in InvIndex:
        return result
    for docs,position in InvIndex[word].items():
        result[docs] = len(position)
    return result

'''
get negated index listing for word in InvIndex
'''
def getNegIndex(word, docSet):
    result = []
    for docs in docSet:
        if docs not in word:
            result.append(docs)
    return result
    
'''
returns the term frequency of word in doc
'''
def tf(doc, word, wordSet, docSet, InvIndex):
    if word.count(' ') == 0 and word in InvIndex:
        if doc in InvIndex[word]:
            return len(InvIndex[word][doc])
    else:
        listDocs = searchBoolean([word], wordSet, docSet, InvIndex)
        word = word.strip().strip('"').strip('(').strip(')').strip()
        if listDocs == None:
            print ''
            print 'Enter a proper search query...'
            print ''
            return ''
        if doc in listDocs:
            return listDocs[doc] // ( word.count(' ') + 1 )
    return 0
    
'''
returns the number of documents, the word appears in
'''
def df(word, wordSet, docSet, InvIndex):
    if word == '':
        print ''
        print 'Enter a proper search query...'
        print ''
        return ''
    if word.count(' ') == 0 and word in InvIndex:
        return len(InvIndex[word])
    else:
        return len(searchBoolean([word], wordSet, docSet, InvIndex))
        
'''
returns the number of times, the word appears in the index
'''
def freq(word, wordSet, docSet, InvIndex):
    if word == '':
        print ''
        print 'Enter a proper search query...'
        print ''
        return ''
    count = 0
    if word.count(' ') == 0 and word in InvIndex:
        for docs in InvIndex[word]:
            count += len(InvIndex[word][docs])
    else:
        listDocs = searchBoolean([word], wordSet, docSet, InvIndex)
        for results in listDocs:
            count += listDocs[results]
        word = word.strip().strip('"').strip('(').strip(')').strip()
        count = count // ( word.count(' ') + 1 )

    return count    
 
'''
returns the words similar to 'word' in the corpus 
similarity is based on frequecy and proximity of other words to the query word
''' 
def similar(docSet, InvIndex, word):
    textS = []
    wordCol = []
    if word not in InvIndex:
        print ''
        print 'Word is not in the index.'
        print ''
        return
    for doc in docSet:
        if doc in InvIndex[word]:
            textS = stemmer(filterData(tokenize(lowercase(parseXML( InvIndex['path_of_documents'] + '/' + 'cranfield' + zfill(str(doc),4) )))))
            textS = [t for t in textS if t != '' ]
            while word in textS and len(wordCol) < 1000:
                index = textS.index(word)
                textS[index] = ''
                wordCol.extend(textS[ (index+1)%len(textS) : (index+4)%len(textS) ] )
                wordCol.extend(textS[ (index-4)%len(textS) : (index-1)%len(textS) ] )
    result = sorted(set(wordCol), key=wordCol.count, reverse = True)
    if len(result) < 10:
        print ''
        print 'List of Similar terms (in stemmed form) is'
        print result
        print ''
    else:
        print ''
        print 'List of Similar terms (in stemmed form) is'
        print result[:10]
        print ''
        

Search Engine Technology HW1

Rohan Agrawal
uni: ra2616

List of Files:
==============
API/Document.py
API/IndexAPI.py
API/porter.py               //from http://tartarus.org/martin/PorterStemmer/index-old.html
API/QueryAPI.py
API/Retreival.py
API/sexpr.py		    //from nltk.tokenize
Index.py
Query.py
Index
Query
README.txt

How to Run:
===========
On the terminal type the following commands

chmod +x Index
chmod +x Query
./Index
./Query

Usage of query:
---------------
The following types of queries are supported:

SearchTerm
----------
e.g. "list matching" problems !pick

tf
--
Syntax: tf DocumentNumber SearchTerm
e.g.  : tf 51 "aerodynamically heated"

df
--
Syntax: df DocumentNumber SearchTerm
e.g.  : df "aerodynamically heated"    

freq
----
Syntax: df DocumentNumber SearchTerm
e.g.  : df "aerodynamically heated"        

title
-----
Syntax: title DocumentNumber
e.g.  : title 51

doc
---
Syntax: doc DocumentNumber
e.g.  : doc 51    

similar
-------
Syntax: similar searchTerm
e.g.  : similar aerodynamics

##NOTE##: Document Number can be given as 51 or 051 or 0051. 
          Valid Document numbers range from 1 to 1400 for the Cranfield Document set.


ARCHITECTURE:

============ 
Runtime Part:
-------------
Index.py
    Takes an argument which specifies the path of documents to be indexed. Writes the index to a file called ra2616Index. Writes metadata to a file called ra2616Metadata
    
Query.py
    Runs the main query loop, asking for user query or request. Usage is given in 'How to Run' section of the readme.
    
API Part:
---------

API/Document.py
---------------
    Contains methods related to reading from documents, processing data before indexing, and getting document snippet from data
 
    Methods:-
    --------
    parseXML(fileName):
     	parses the file given in fileName, returns text in string
    getMetadata(fileName):
     	returns the meta data of the fileName in a dictionary, keys are xml tags 'DOCNO','BIBLIO','AUTHOR'
    stemmer(word):
     	returns the stemmed version of words in a list word
    tokenize(string):
     	returns  tokens in a list from string input
    lowercase(word):
     	returns lowercase of words in a list word
    filterData(word):
     	returns words in list word after removing full stops and commas
    printDocument(file, title = False)):
     	prints the contents of given file, prints only title, if the second argument is provided as false
    matches(searchFor,searchIn):
     	returns the number of times searchFor string occurs in searchIn string
    getSnippets(topDocs, InvIndex, searchFor):
     	returs the snippets of length 30 from documents in topDocs. The snippets are returned on the basis of 
	maximum number of occurences of searchFor terms in the snippet.
    printDoc(docs, path):
     	prints the contents of docs stored in path
    printTitle(docs, path):
     	prints the Title of docs stored in path
     
API/IndexAPI.py
---------------
    Contains methods related to creation and storage of Inverted Index as well as storage of metadata
 
    Methods:-
    --------
    invertedListAppend( words, doc, InvertedIndex ):
     	appends the list of words given in words, into the invertedIndex, under the given doc document name
    writeIndexToFile(fileName, InvertedIndex):
     	Writes the invertedIndex to file fileName
    MakeIndex(path):
     	takes an input path, reads all data from files in the path, and appends to inverted index after 
	processing data. Returns the constructed inverted index
    storeMetadata(path,fileName):
     	takes app file in path, stores the metadata in a dictionary and writes the dictionary to fileName through JSON
     
API/porter.py   
-------------            
    Code taken from http://tartarus.org/martin/PorterStemmer/index-old.html
    PorterStemmer().stem(word,startIndex,EndIndex) method stems the given word in between start and end indices

API/sexpr.py
------------
   Code taken from nltk.tokenize. Tokenizes an expression, leaving the expressions in-tact. 
   E.g. 'abc "def ghi"' is tokenized as ['abc', '"def ghi"']
    
API/QueryAPI.py
---------------
    Contains methods required for processing the query, sorting the results dictionary recieved from Document.py and printing final results
    
    Methods:-
    --------
    flatten(list):
     	flatten a nested list: e.g. [a,b,[c,d]] => [a,b,c,d]
    parseSearchString(searchString):
     	split search string into seperate words, phrases and returns list of seperate words, phrases
    sortByValue(x):
     	sorts a dictionary by value and return sorted list 
    printResults(top5, snippets, round):
     	prints search results in a formatted way, with snippets and rank of document
    preprocess():
     	Reads the index from ra2616Index into a dictionary, and makes set of documents and words. 
	Returns all 3 data structures, (wordSet, docSet, InvIndex)
     
API/Retreival.py
----------------
    Contains methods related to retreival of search results, calculation of best documents for given query, calulation of tf, df, freq, similar methods.
    
    Methods:-
    --------
    searchBoolean(searchTerms, wordSet, docSet, InvIndex):
     	performs the main boolean search function, for terms in searchTerms. Returns a dictionary whose key 
	is documentID, value is score
    phraseSearch(phrase, wordSet, docSet, InvIndex):
     	performs phrase search, returns a dictionary whose key is docuentId and value is number of occurences 
	of the phrase in the document.
    phraseMerge(list1, list2):
     	merges two lists, list1 and list2 and returns merged list. Merged list contains documents which contain 
	words from list1 and 2 next to each other.
    simpleMerge(list1, list2):
     	merges list1 and list2, combining scores for each document in the list. Equivalend to fuzzy OR. 
	Returns the merged list.
    getIndex(word, InvIndex):
     	get index listing for word in InvIndex
    getNegIndex(word, docSet):
     	get negated index listing for word in InvIndex
    tf(doc, word, wordSet, docSet, InvIndex):
     	get term frequency of word in doc
    df(word, wordSet, docSet, InvIndex):
     	get document frequency of word in InvIndex
    freq(word, wordSet, docSet, InvIndex):
     	get frequency of word in InvIndex
    similar(docSet, InvIndex, word):
     	returns a list of similar words to the word, based on frequency and proximity to the query word.
    
         

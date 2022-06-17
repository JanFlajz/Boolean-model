import random
from collections import defaultdict
from pyeda.inter import *
import math
import heapq
import timeit
import os, sys
from django.core.files import File
from django.conf import settings

allWords = defaultdict(list)
allSongs = defaultdict(list)
module_dir = os.path.dirname(os.path.abspath(__file__))
shouldPreprocess = True
# Class for encapsuling author and name into a single entity 'Song'
class Song:
    def __init__(self, author, name):
        self.author = author
        self.name = name

# Class for better orientation when searching if a song has the requested words.
# As long as it's misleading, it's not actually a linked list but rather a dictionary.
# It used to be a linked list, but the effectiveness was like 180x times worse
class SongHolder:
    def __init__(self):
        self.ll = {}

    # insertion method
    def insert(self, songID, relevancy):
        self.ll[songID] = relevancy

    # check-up for an element. If the element is present, returns number of occurances, else returns 0
    def getRelevancy(self, data):
        if self.ll.get(data) is None:
            return float(0)
        else:
            return float(self.ll.get(data))

# Loads all words from a given file and fills allWords, fMaxDict and dfi
# allWords is a list of all words
# fMaxDict is a list of the word's max occurances
# dfi - for more info look at vector model in VWM slides
def allWordsFunc(allWords, linkedWords):
    #with open('../Dataset/linkedWords.txt') as coreWordsDoc:
        coreWordsDoc = linkedWords
        coreWordsString = coreWordsDoc.read()
        coreWordsLines = coreWordsString.split('\n')
        coreWordsLines.pop()
        for line in coreWordsLines:
            coreWords = line.split('<SEP>')
            tmpLL = SongHolder()
            record = coreWords[4].split(',')
            for ww in record:
                pair = ww.split(':')
                tmpLL.insert(pair[0], pair[1])
            allWords[coreWords[1]] = tmpLL

# Reads all songs from a file and parses them into the given allSongs list
def allSongsFunc(allSongs, songList):

    #with open('../Dataset/songList.txt') as SongListDoc:
        SongListDoc = songList
        songListString = SongListDoc.read()
        p = 0
        songListLine = songListString.split('\n')
        for lineString in songListLine:
            p += 1
            if p == len(songListLine):
                continue
            line = lineString.split('<SEP>')
            #allSongs[line[3]] = Song(line[4], line[5])
            # TODO: When our stemming goes live, use the following line instead:
            allSongs[line[0]] = Song(line[1],line[2])

# Calculating relevancy of a desired song
def calcRelev(e, allWords, searhcedSong):
    argCount = 0
    ans = 0
    # -------OR()-------
    if e.ASTOP == "or":
        # Serves for calling And function and then wrap it all up and compute the overall relevancy
        for orArg in e.xs:
            argCount += 1

            # -------OR(And())-------
            if orArg.ASTOP == "and":
                argCountAnd = 0
                ansAnd = 0

                for andArg in orArg.xs:
                    argCountAnd += 1
                    if andArg.name not in allWords:
                        continue
                    ansAnd += math.pow(
                        (1 - (allWords[andArg.name]).getRelevancy(searhcedSong)), 2)
                ans += 1 - math.sqrt(ansAnd / argCountAnd)
            else:
                if orArg.name not in allWords:
                    continue
                else:
                    ans += ((allWords[orArg.name]).getRelevancy(searhcedSong))
        if ans < 0:
            return 0
        else:
            return math.sqrt(ans / argCount)

    # -------And()-------
    elif e.ASTOP == "and":
        argCount += 1
        argCountAnd = 0
        ansAnd = 0

        for andArg in e.xs:
            argCountAnd += 1
            if andArg.name not in allWords:
                continue
            ansAnd += math.pow(
                (1 - (allWords[andArg.name]).getRelevancy(searhcedSong)), 2)

        ans += 1 - math.sqrt(ansAnd / argCountAnd)

    # Just single argument as a question
    # -------WORD-------
    else:
        if e.name not in allWords:
            return 0
        return (allWords[e.name]).getRelevancy(searhcedSong)
    return ans

def processInput(expression,allWords):
    expressionWords = []
    tmp = []
    if expression.ASTOP == "or":
        for orArg in expression.xs:
            if orArg.ASTOP == "and":
                for andArg in orArg.xs:
                    expressionWords.append(andArg.name.lower())
            else:
                expressionWords.append(orArg.name.lower())
    elif expression.ASTOP == "and":
        for andArg in expression.xs:
            expressionWords.append(andArg.name.lower())
    else:
        expressionWords.append(expression.name.lower())
    toDelete = []
    for word in expressionWords:
        if word not in allWords:
            toDelete.append(word)
    for toDel in toDelete:
        expressionWords.remove(toDel)
    for word in expressionWords:
        ll = allWords[word].ll
        for wordDoc in ll:
            tmp.append(wordDoc)
    relevantSongs = list(dict.fromkeys(tmp))
    return relevantSongs

def webFunc(number, relevancies,allSongs):
    # -------Sorting and picking the TOP {number}-------
    res = heapq.nlargest(number, relevancies, key=relevancies.get)
    resultList = []

    # If there are not viable songs for the search
    if len(res) == 0 or relevancies[res[0]] == 0:

        # Picking random {number} songs
        tmp = random.sample(allSongs.keys(), number)
        print(len(allSongs.keys()))
        for result in tmp:
            resultList.append(allSongs[result])
        return resultList

    # Else if there are viable songs
    else:
        for result in res:
            resultList.append(allSongs[result])
        return resultList



def preprocess(songList, linkedWords):
    # ------INITIALIZATION-------


    tmp = 0
    # -------PREPROCESSING-------
    start = timeit.default_timer()

    allSongsFunc(allSongs, songList)
    allWordsFunc(allWords,linkedWords)
    stop = timeit.default_timer()
    print('Preprocessed in ', stop - start)

def searchSongs(numOfResults, expression):
    start = timeit.default_timer()
    relevancies = defaultdict(list)
    ands = []
    pp = 0
    print("Welcome! What's on your mind?")
    val = str(expression)
    print(val)
    print(numOfResults)
    e = expr(val).to_dnf()
    relevantSongs = processInput(e, allWords)
    # -------Calculating relevancies for all songs (documents)-------
    for song in relevantSongs:
        relevancies[song] = calcRelev(e, allWords, song)

    ans = webFunc(numOfResults, relevancies, allSongs)
    for answer in ans:
        print(answer.name + " | " + answer.author)
    stop = timeit.default_timer()
    print('Found ',numOfResults, ' results in ' , stop - start)    
    return ans


'''
# -------MAIN-------
if __name__ == '__main__':
    # ------INITIALIZATION-------
    allWords = defaultdict(list)
    allSongs = defaultdict(list)
    tmp = 0
    # -------PREPROCESSING-------
    start = timeit.default_timer()

    allSongsFunc(allSongs)
    allWordsFunc(allWords)
    stop = timeit.default_timer()
    print('Preprocessed in ', stop - start)

    # -------MAIN ENDLESS LOOP-------
    while True:
        relevancies = defaultdict(list)
        ands = []
        pp = 0
        print("Welcome! What's on your mind?")
        val = input()
        e = expr(val).to_dnf()
        relevantSongs = processInput(e,allWords)
        # -------Calculating relevancies for all songs (documents)-------
        for song in relevantSongs:
            relevancies[song] = calcRelev(e, allWords, song)

        ans = webFunc(10,relevancies,allSongs)
        for answer in ans:
            print(answer.name + " | " + answer.author)
'''

import math
from collections import defaultdict
import timeit

# Computing fMAX
# Making updating linkedWords.txt with fMax
def computefMax():
    input = open('./../Dataset/linkedWords.txt', 'r')
    splittedDoc = input.read().split('\n')
    splittedDoc.pop()
    with open('./../Dataset/linkedWords.txt', 'w') as output:
        for i in splittedDoc:
            tmpFMax = 0
            firstIterationBool = True
            lineSplit = i.split('<SEP>')
            songs = lineSplit[2].split(',')
            # looking at each pair song:numberOfOcc
            for pair in songs:
                doubles = pair.split(':')
                # If numberOfOcc is better than our tmpFMax, rewrite our max to new max.
                if int(doubles[1]) > tmpFMax:
                    tmpFMax = int(doubles[1])
            splitStr = i.split('<SEP>')
            output.write(splitStr[0] + "<SEP>" + splitStr[1] + "<SEP>" + str(tmpFMax) + "<SEP>" + splitStr[2] + '\n')

# Making linkedWords.txt from Dataset/topWords and Dataset/occSet
def createCoreWords():
    global list
    with open('./../Dataset/topWords.txt', 'r') as wordDocument:
        wordDoc = wordDocument.read()
        words = wordDoc.split(',')
        iterator = 1
        # A dictionary with wordID:word
        wordDictionary = dict()
        for word in words:
            wordDictionary[iterator] = word
            iterator += 1
        finalDict = defaultdict(list)
        with open('./../Dataset/occSet.txt') as WordOccurancesDoc:
            songIterator = 0

            WordOccurances = WordOccurancesDoc.read()
            lineSplit = WordOccurances.split('\n')
            lineSplit.pop()
            for line in lineSplit:
                information = line.split('<SEP>')
                for infWord in information[1].split(','):
                    sepinf = infWord.split(':')
                    list = [information[0], sepinf[1]]
                    finalDict[sepinf[0]].append(list)
                songIterator += 1

            # Writing in the file
            outputFile = open('./../Dataset/linkedWords.txt', "w")
            for answer in sorted(finalDict):
                outputFile.write(answer + "<SEP>" + wordDictionary[int(answer)])
                first = True
                for hehe in sorted(finalDict[answer]):
                    if first:
                        outputFile.write("<SEP>")
                        first = False
                    else:
                        outputFile.write(",")
                    outputFile.write(hehe[0] + ":" + hehe[1])
                outputFile.write("\n")
            outputFile.close()

def computeDFI():
    dfi = defaultdict()
    dfi['xxx'] = 'grandson'
    with open('./../Dataset/linkedWords.txt', 'r') as coreWordsDoc:
        coreWordsString = coreWordsDoc.read()
        coreWordsLines = coreWordsString.split('\n')
        i = 0
        for line in coreWordsLines:
            i += 1
            if i == len(coreWordsLines):
                continue
            coreWords = line.split('<SEP>')
            tmp = 0
            test = coreWords[3].split(',')
            for ww in test:
                tmp += 1
            dfi[coreWords[1]] = int(tmp)
    file = open('./../Dataset/linkedWords.txt', 'r')
    coreWordsLines = (file.read()).split('\n')
    i = 0
    dfi.pop('xxx')
    with open('./../Dataset/linkedWords.txt','w') as outputWordsDoc:
        for line in coreWordsLines:
            i += 1
            if i == len(coreWordsLines):
                continue
            coreWords = line.split('<SEP>')
            tmp = coreWords[len(coreWords)-1]
            coreWords[len(coreWords)-1] = str(dfi[coreWords[1]])
            for information in coreWords:
                outputWordsDoc.write(information)
                outputWordsDoc.write('<SEP>')
            outputWordsDoc.write(tmp)
            outputWordsDoc.write('\n')

def computeRelevancies(n):
    input = open('./../Dataset/linkedWords.txt', 'r')
    coreWordsString = input.read()
    coreWordsLines = coreWordsString.split('\n')
    with open('./../Dataset/linkedWords.txt', 'w') as outputDoc:
        inc = 1
        for line in coreWordsLines:
            if inc == len(coreWordsLines):
                continue
            inc += 1
            newPairList = defaultdict()
            newPairList['xxx'] = 0.5
            splitLine = line.split('<SEP>')
            documentList = (splitLine[len(splitLine)-1]).split(',')
            for document in documentList:
                pair = document.split(':')
                # calculating Relevancy as : ( fij / max{fij} ) * log2 ( n / dfi )
                x = (int(pair[1]) / int(splitLine[2])) * math.log2(n / int(splitLine[3]))
                newPairList[pair[0]] = round(x,7)
            splitLine.remove(splitLine[len(splitLine)-1])
            for i in splitLine:
                outputDoc.write(i)
                outputDoc.write('<SEP>')
            first = True
            newPairList.pop('xxx')
            for pair in newPairList:
                if not first:
                    outputDoc.write(',')
                outputDoc.write(str(pair))
                outputDoc.write(':')
                outputDoc.write(str(newPairList[pair]))
                first = False
            outputDoc.write('\n')

if __name__ == '__main__':
    start = timeit.default_timer()
    print("hi")
    createCoreWords()
    print("createCoreWords Finished!")
    computefMax()
    print("computefMax Finished!")
    computeDFI()
    print("computeDFI Finished!")
    n = sum(1 for line in open('./../Dataset/songList.txt'))
    computeRelevancies(n)
    print("computeRelevancies Finished!")
    stop = timeit.default_timer()
    print("Total time: " + str(stop-start))


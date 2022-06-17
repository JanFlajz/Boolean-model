import re
# dictionary that converts ISO639-1 to language name for stemming https://gist.github.com/alexanderjulo/4073388
import languages_and_countries

from nltk import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
# language detection
from langdetect import *

import sys
import os
import io
# removes embed in the end
embed = 6
# removes header
lrcs = 6

#length of last comma to remove
commaLen = 1
#start id of words
idWord = 0



 
class CWord:
    def __init__(self, word, id):
        self.word = word
        self.id = id
        self.occurence = 1


allWords = set()



class CSong:


    def __init__(self, id, artist, name):
        self.id = id
        self.artist = artist
        self.name = name
        self.usedWords = set()
        self.wordList = ""
        self.numOfTopWords = 0

    def insertLyrics(self, word, occurence):
        list = (word, occurence)
        self.usedWords.add(list)

    def createWordlist(self, topWords):
        file_str = io.StringIO()
        file_str.write(self.id)
        file_str.write("<SEP>")

        for word in topWords:
            w = [k for k in self.usedWords if word.word == k[0].word]
            if(len(w) >0):
                self.numOfTopWords += 1
                file_str.write(str(word.id))
                file_str.write(":")
                file_str.write(str(w[0][1]))
                file_str.write(",")

        self.wordList = file_str.getvalue()
        if self.numOfTopWords <= 0:
            return ''
        self.wordList = self.wordList[0: len(self.wordList) - (commaLen)]
        self.wordList += "\n"
        return self.wordList


songs = set()


def createSongLyricsList(lyrics, song, idWord):
    uniqueWords = set()
    # create unique words in lyrics
    for w in lyrics:

        uniqueWords.add(w)
        isnew = [k for k in allWords if k.word == w]
        if len(isnew) == 0:
            newWord = CWord(w, idWord)
            allWords.add(newWord)
            occ = lyrics.count(w)
            song.insertLyrics(newWord, occ)
            idWord += 1
        else:
            isnew[0].occurence += 1

    songs.add(song)


#set english stop words in case language detection doesnt work properly https://gist.github.com/sebleier/554280
defaultStopWords = {
"0o", "chrous", "Strophe", "Refrain" ,"0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"
}

def proccessLyrics(lyrics, song, idWord):
    start = lyrics.find("Lyrics")

    lyrics = lyrics[start + lrcs:len(lyrics) - embed]
    # delete some bracktes content
    lyrics = re.sub(r'\([^)]*\)', '', lyrics)
    # make sure all square brackets were deleted
    lyrics = re.sub(r'\[[^\]]*\]', '', lyrics)


    try:
        DetectorFactory.seed = 0
        l = detect(lyrics)
    except:
        return

    i = [item for item in languages_and_countries.languages if item[0] == l]
    try:
        lang = i[0][1]
    except:
        return

    lang = lang.lower()
    if lang not in stopwords.fileids():
        return


    tokenizer = RegexpTokenizer(r'\w+')
    # removes interpunkts
    try:
        lrcsPunkt = tokenizer.tokenize(lyrics)
    except:
        return
    # remove stopwords
    try:
        stopWords = defaultStopWords.union(set(stopwords.words(lang)))
        #somehow doesnt detect this word

    except:
        return

    filtered = []
    #filter stop words
    for w in lrcsPunkt:

        if w not in stopWords and len(w) != 1 and type(w) != int:
            filtered.append(w)
    try:
        snowballStemmer = SnowballStemmer(lang)
    except:
        return
    result = []
    for w in filtered:
        try:
            x = snowballStemmer.stem(w)
        except:
            return
       
        result.append(x)
    print(result)
    
    createSongLyricsList(result, song, idWord)


def readLyrics(idWord):
    with open("realDataSet/proccesedLyrics.txt", 'r+') as lyricsFile:

        r = re.compile('.*<SEP>.*<SEP>')
        file_str = io.StringIO()
        song = CSong(0, "", "")
        num = 1
        for line in lyricsFile:
            if line == "----NEWSONG----\n":
                if file_str.getvalue() != "":
                    print("working on song num:", num, "id: ", song.id)
                    num += 1
                    proccessLyrics(file_str.getvalue(), song, idWord)
                file_str = io.StringIO()
            else:
                if re.match(r, line):
                    info = line.split('<SEP>')
                    song = CSong(info[0], info[1], info[2])

                    file_str.write(line)

    lyricsFile.close()


if __name__ == '__main__':


    if len(sys.argv) < 2:
        exit(0)

    readLyrics(idWord)

    times = int(sys.argv[1])
    ratio = int(sys.argv[2])

    finalstopWordsCount = (times/ratio) * 100




    #created topwords
    sortedWords = sorted(allWords, key=lambda x:x.occurence, reverse=True)
    topWords = sortedWords[:((int(len(sortedWords)) * times)/ratio)]
    id = 1
    for word in topWords:
        word.id = id
        id += 1

        # create top words List

    file_str = io.StringIO()
    dir = '../OurDataset/Dataset/'


    os.mkdir(dir)

    topWordsPath = dir + 'topWords.txt'
    with open(topWordsPath, 'w+') as wordList:

        for w in topWords:
            file_str.write(w.word)
            file_str.write(",")
        topWordsString = file_str.getvalue()
        topWordsString = topWordsString[:len(topWordsString) - commaLen]
        wordList.write(topWordsString)
    wordList.close()
    print("topwords done")
    # create top words List
    occSetPath = dir + 'occSet.txt'
    with open(occSetPath, "w+") as occSet:
        for song in songs:
            occSet.write(song.createWordlist(topWords))
    occSet.close()
    print("occ set done")

    songlistPath = dir + 'songList.txt'
    #creates Song List
    with open(songlistPath, 'w+') as songList:
        for song in songs:
            if song.numOfTopWords > 0:
                song.name = song.name[:len(song.name) -1]
                songList.write(str(song.id) + "<SEP>" + song.name + "<SEP>" + song.artist + "\n" )
    songList.close()
    print("songlist done")

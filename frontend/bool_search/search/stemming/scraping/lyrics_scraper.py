import lyricsgenius
from lyricsgenius import Genius
token = "F-oNHJihRlNmXds-osTVVuQ2bSRvZrr109N3Z9nU4hEXj7YjU6xTfCuR1Y1UZVYZ"
songSep = "----NEWSONG----\n"

genius = lyricsgenius.Genius(token)


#change name to form without brackets
def repairName(name):

    result =name.find('(')
    #creates substring
    if result != -1:
        name = name[:result]
    return name


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    song = genius.search_song("Super Cayor De Dakar","Capitale  ",383571)
    print(song.lyrics)



    '''
    #read original songlist
    genius = Genius(token)
    with open('songlist.txt','r+') as songlist:
        lines = songlist.readlines()
        with open('betterSongList.txt', 'w+') as outputSongList:
            with open('songLyrics.txt', 'w+') as lyricsFile:
                for line in lines:
                    info = line.split('<SEP>')
                    artist = info[4]
                    if(info[5][0] == '(' or info[5][0] == '['):
                        continue
                    title = info[5]
                    title = title[:title.__len__() -1]
                    title = repairName(title)
                    try:
                        song = genius.search_song(title,artist)
                    except:
                        pass
                    if(song == None):
                        continue
                    outputSongList.write(str(song.id) + "<SEP>" + artist+ "<SEP>" + title + "\n")
                    lyricsFile.write(songSep)
                    lyricsFile.write(str(song.id) + "<SEP>" + artist + "<SEP>"+ title + "\n" + song.lyrics + "\n")

            lyricsFile.close()
        outputSongList.close()
    songlist.close()
    '''






    #genius.search_artist('Andy Shauf')
    #artist = genius.search_artist("Andy Shauf", 3, "title")




# See PyCharm help at https://www.jetbrains.com/help/pycharm/

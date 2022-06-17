import lyricsgenius
from lyricsgenius import Genius

token = "F-oNHJihRlNmXds-osTVVuQ2bSRvZrr109N3Z9nU4hEXj7YjU6xTfCuR1Y1UZVYZ"
songSep = "----NEWSONG----\n"

if __name__ == '__main__':
    genius = Genius(token)
    with open('authorlist.txt', 'r+') as songlist:
        lines = songlist.readlines()

        with open('../realDataSet/songlyrics.txt', 'w+') as lyricsFile:
            for line in lines:
                author = None
                try:
                    author = genius.search_artist(line)
                except:
                    pass
                if (author == None):
                    continue
                line = line[:len(line) - 1]
                print(line)
                for song in author.songs:
                    lyricsFile.write(songSep)
                    lyricsFile.write(str(song.id) + "<SEP>" + line + "<SEP>" + song.title + "\n" + song.lyrics + "\n")

            lyricsFile.write(songSep)

        lyricsFile.close()

songlist.close()

from django.shortcuts import render
import sys, os

from .extendedBoolean import main
from .preProccess import *
from django.core.files import File
import sys
sys.path.append("..")
from django.conf import settings

shouldPreProcess = True


# Create your views here.
def printResults(request):
    topSongs = []
    if request.method == 'POST':
        expression =request.POST.get('inputTextField')
        numOfResults =request.POST.get('choices-single-defaul')
        numOfResults = int(numOfResults)
        #get values from backend
        print(numOfResults)
        print(expression)
        result = main.searchSongs(numOfResults,expression)
        shouldPreProcess = False
        for song in result:
            searchedSong = ""
            searchedSong += song.author
            searchedSong += " by "
            searchedSong += song.name
            topSongs.append(searchedSong)

        
        return render(request, 'results.html', {'topSongs' : topSongs, 'searchedFor' : expression, 'numOfResults' : len(topSongs)})


def home(request):
    return render(request, 'home.html', {})

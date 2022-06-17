#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from search.extendedBoolean import main as ext
from django.conf import settings



def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bool_search.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    print("Hello")
    with open('../bool_search/search/Dataset/songList.txt') as songList:
        with open('../bool_search/search/Dataset/linkedWords.txt') as linkedWors:
            ext.preprocess(songList, linkedWors)
        linkedWors.close()
    songList.close()
    
    main()

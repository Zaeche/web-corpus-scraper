# -*- coding: UTF-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""
Author: Zeeshan Shahid
Last Date Modified: 03/03/2018
"""""""""""""""""""""""""""""""""""""""""""""""""""

import re, os, glob, string
from random import randint
from collections import OrderedDict

file_names = []
clean_files = []
fpath = r"D:\GitHub\web-corpus-scraper\alt_cor"

def CleaningPass():
    text_files = [_ for _ in (os.listdir(fpath)) if _[-4:] == ".txt"]

    for out in text_files:
        file_names.append(out)
        with open (out, "rb") as textFile:
            lines = (line.rstrip() for line in textFile)
            unique_lines = OrderedDict.fromkeys( (line for line in lines if line) )

        history, textData = set(), []
        keyses = (r"".join(unique_lines.keys()))

        # remove repeats
        for word in unique_lines.keys():
            if word not in history:
                textData.append(word + " ")
                history.add(word)

        textData = "\r\n".join(textData)
        textData = re.sub(r"(?:\@|https?\://)\S+", "", textData) # remove links and urls
        textData = re.sub(r"(\d\:\d+\s\w+)|(\d+\s\w+\s\d+)|(\d\s\w+)(?=notes)|(•)|(\d)|(notes)", "", textData)

        textData = ''.join(ch for ch in textData if ch not in set(string.punctuation)) # remove punctuation
        textData = re.sub(r"(\d\:\d+\s\w+)|(\d+\s\w+\s\d+)|(\d\s\w+)(?=notes)|(•)|(\d)|(notes)", "", textData)

        cleaned = "clean_" + out
        clean_files.append(cleaned)
        #file_names.append(cleaned) # disabled for debug
        with open(cleaned, "wb") as cleanText:
            cleanText.write(textData)

def main():
    for _ in range(2):
        CleaningPass()

    for f in clean_files: #change to file_names after debug is complete
        os.remove(f)
    return 0

if __name__ == '__main__':
    main()





"""
References and misc:
http://stackoverflow.com/a/13896637 'J.F Sebastian'
http://stackoverflow.com/questions/31222137/how-to-get-name-of-a-file-in-directory-using-python
http://stackoverflow.com/questions/15830290/remove-duplicates-from-text-file "StuGrey"

#textData = re.sub(r"(\d\:\d+\s\w+)|(\d+\s\w+\s\d+)|(\d\s\w+)(?=notes)|(•)|(\d)|(notes)", "", textData)
"""

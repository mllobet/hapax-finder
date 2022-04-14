#!/usr/bin/env python3

import argparse
import sys

from os import listdir
from os.path import isfile, join

from collections import defaultdict

# Removes all unwanted characters
def clean_word(word):
    # remove all caps words
    no_caps = ''.join(filter(lambda c: not c.isupper(), word))
    if no_caps == '':
        return ''

    # remove URLs
    # www
    if len(word) >= 3:
        if word[:3] == "www":
            return ''
    # http
    if len(word) >= 4:
        if word[:4] == "http":
            return ''

    clean = ''.join(filter(str.isalnum, word))
    clean = ''.join(filter(lambda c: c.isalpha(), clean))

    # transform to lowercase
    clean = clean.lower()


    # print("BEFORE {} AFTER {}".format(word, clean))

    return clean

# Finds happaxes given a text file
# Returns a dictionary containing all hapaxes
def find_hapax(file):
    d = defaultdict(lambda: 0)
    
    found_start = False
    for line in file:

        if not found_start:
            found_start = len(line) >= 3 and line[:3] == "***"
            pass

        for word in line.split(' '):
            clean_w = clean_word(word)
            d[clean_w] += 1

    hapaxes = dict(filter(lambda elem: elem[1] == 1, d.items()))
    # print(hapaxes)
    return hapaxes

def run(files, directory):
    # flatten files
    directory_files = []
    if directory:
        directory_files = [f for f in listdir(directory) if isfile(join(directory, f))]
    all_files = files + directory_files 

    # run hapax finder for each file
    for file in files:
        with open(file, 'r') as f:
           hapax_dict = find_hapax(f)
           print("Hapax count: {}".format(len(hapax_dict)))
           for k, v in hapax_dict.items():
               print(k)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finds words that appear only once in a given text (hapaxes)")
    parser.add_argument('-f', '--file', help="the file(s) to check for hapaxes on", nargs='+', default=[])
    parser.add_argument('-d', '--directory', help="the directory of text files to check for hapaxes on") 

    args = parser.parse_args(sys.argv[1:])
    print (args)
    run(args.file, args.directory)

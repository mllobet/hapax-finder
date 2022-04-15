#!/usr/bin/env python3

import argparse
import sys

from os import listdir
from os.path import isfile, join

from collections import defaultdict

# Removes all unwanted characters
def clean_word(word):

    # remove URLs
    # www
    if len(word) >= 3:
        if word[:3] == "www":
            return ''
    # http
    if len(word) >= 4:
        if word[:4] == "http":
            return ''

    # keep only letters, no numbers/punctuation
    clean = ''.join(filter(lambda c: c.isalpha(), word))

    # remove all caps words
    no_caps = ''.join(filter(lambda c: not c.isupper(), clean))
    if no_caps == '':
        return ''

    # transform to lowercase
    clean = clean.lower()


    #print("---\nBEFORE {} AFTER {}\n".format(word, clean), file=sys.stderr)

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

def run(files, input_directory, output_directory):
    # flatten files
    directory_files = []
    if input_directory:
        directory_files = [input_directory + '/' + f for f in listdir(input_directory) if isfile(join(input_directory, f))]
    all_files = files + directory_files 

    # run hapax finder for each file
    for file in all_files:
        print(file)
        with open(file, 'r') as f:
            # rename outfile
            outfile = file.replace("txt", "hx")
            i = outfile.find('/')
            if i >= 0:
                outfile = output_directory + '/' + outfile[i+1:]

            with open(outfile, 'w') as w:
                hapax_dict = find_hapax(f)
                print("Hapax count: {}".format(len(hapax_dict)))
                for k, v in hapax_dict.items():
                    w.write(k + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finds words that appear only once in a given text (hapaxes)")
    parser.add_argument('-f', '--file', help="the file(s) to check for hapaxes on", nargs='+', default=[])
    parser.add_argument('-d', '--directory', help="the directory of text files to check for hapaxes on", default="") 
    parser.add_argument('-o', '--output-dir', help="the output directory to store hapax files", default="hapaxes")

    args = parser.parse_args(sys.argv[1:])
    print (args)
    run(args.file, args.directory, args.output_dir)

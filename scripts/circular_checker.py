#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Check if a sequence is circular or not, using Knutt-Morris-Pratt array.

Usage:
    ./circular_checker.py <sequences> (--output=<file>) [options]

Options:
    --format, -f=<string>   The file format [default: fasta]
    --help, -h              Display this screen.
    --output, -o=<file>     Name of the output file (erase if already exist)
    --size,-s=<int>         Sequences minimum length allowed [default: 1500]
    --threshold, -t=<int>   Threshold limit to decide if the sequence is circular or not [default: 20]
    --version,-v            Script version
"""

##########
# IMPORT #
##########
import os

from docopt import docopt
from Bio import SeqIO

########
# MAIN #
########
def main(args):
    """
    Just a regular main, which call all the differents functions, and do 
    barely nothing else (matters).
    """
    result_seq = []
    # Sequences extraction
    print("1) Extracting the sequences")
    list_seq = _extract_sequences(args["<sequences>"], args["--format"])
    # Analyse seq one by one
    print("2) Computing the KMP array for each sequence")
    for seq in list_seq:
        if len(seq.seq) >= int(args["--size"]):
            kmp_array = _kmp_array(seq.seq)
            if kmp_array[-1] >= int(args["--threshold"]):
                seq.description = seq.description+" overlap: "+str(kmp_array[-1])
                result_seq.append(seq)
    # Output file
    print("3) Writing "+args["--output"])
    _print_file(result_seq, args["--format"], args["--output"])

#############
# FUNCTIONS #
#############
def _extract_sequences(path_file, file_format):
    """
    Extract all infos from the sequences file.
    """
    # A generator, juste because it's beautifull
    label_list = [sequence for sequence in
                  SeqIO.parse(os.path.abspath(path_file), file_format)]
    return label_list

def _kmp_array(sequence):
    """
    Take a string and compute a Knuth-Morris-Pratt array.
    Return a list.
    """
    seq_size = len(sequence)
    array = [0]*seq_size
    # Creation of the array
    for index in range(1, seq_size):
        if sequence[index] == sequence[array[index-1]]:
            array[index] = array[index-1]+1
    return array

def _print_file(selected_seq, seq_type, output):
    """
    selected_seq: a list
    seq_type: string
    output: file path
    """
    output_file = open(output, "w")
    SeqIO.write(selected_seq, output_file, seq_type)
    output_file.close

##########
# LAUNCH #
##########
if __name__ == "__main__":
    args = docopt(__doc__, version="1.0")
    main(args)

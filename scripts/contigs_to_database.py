#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
BLABLA

Usage:
    ./contigs_to_database.py <directory> (--output=<file>) [options]

Options:
    --format, -f=<string>   The files format [default: fasta]
    --help, -h              Display this screen.
    --output, -o=<file>     Name of the output file (erase if already exist)
    --version,-v            Script version
"""

##########
# IMPORT #
##########
import os
import glob

from docopt import docopt
from Bio import SeqIO

########
# MAIN #
########
def main(args):
    """
    Look inside each file, adapt the name of the sequence and create the
    contigs database.
    """
    # Creating the output file
    output_file = open(args["--output"],"w")
    # Checking each contig file
    for contig_file in glob.glob(args["<directory>"]+"/*/contigs.*"+args["--format"]):
        extract = contig_file.split("/")[-2]
        # One file after an other
        print("Working on:")
        print(extract)
        list_seq = _extract_sequences(contig_file, args["--format"])
        for seq in list_seq:
            seq.id = extract+"_"+seq.id
            seq.description=""
            SeqIO.write(seq, output_file, args["--format"])
    output_file.close()


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

##########
# LAUNCH #
##########
if __name__ == "__main__":
    args = docopt(__doc__, version="1.0")
    main(args)

#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Manage the analysis of a contigs set obtained from a sample.

Usage:
    ./metavirome_analysis.py <dir>

Options:
    --help, -h              Display this screen
    --version, -v           Show version

"""

##########
# IMPORT #
##########
import os

from docopt import docopt

########
# MAIN #
########
def main(args):
    path_contig = os.path.abspath(args["<dir>"]+"contigs.fasta")
    print("\n"+path_contig.split("/")[-2])
    # First: check the potential circular contigs
    if "circular_contigs.fasta" not in os.listdir(args["<dir>"]):
        print("Check potential circular contigs")
        os.system("./scripts/circular_checker.py "+path_contig+
              " -o "+args["<dir>"]+"circular_contigs.fasta")
    else:
        print("Circular contigs already estimated.")
    # Find ORF
    if "orf.fasta" not in os.listdir(args["<dir>"]):
        print("Find ORF in each contigs")
        os.system("./scripts/orf_finder.py "+path_contig+
              " -o "+args["<dir>"]+"orf.fasta")
    else:
        print("ORFs already calculated")
    # Alignement on database
    if "alignement.csv" not in os.listdir(args["<dir>"]):
        if os.listdir("database") == []:
            print("Their is no database file in the database directory, alignement is impossible")
        else:
            i=0
            for db in os.listdir("database/"):
                if db[-4:]=="dmnd":
                    i+=1
                    os.system("./diamond blastp -q "+args["<dir>"]+
                              "orf.fasta -d database/"+db+" -a tmp_result")
                    os.system("./diamond view -a tmp_result.daa -o "+
                              args["<dir>"]+"alignement.csv")
                    os.system("rm tmp_result.daa")
            if i==0:
                print("No database in .dmnd format found, please use format_database.sh")
    else:
        print("Contigs already aligned.")
    # Visualisation by Krona
    if "krona_results.html" not in os.listdir(args["<dir>"]):
        os.system("./krona/scripts/ImportBLAST.pl "+args["<dir>"]+"alignement.csv"+
                  " -o "+args["<dir>"]+"krona_results.html")
    else:
        print("Visualisation already available.")

##########
# LAUNCH #
##########
if __name__ == "__main__":
    args = docopt(__doc__, version="1.0")
    main(args)

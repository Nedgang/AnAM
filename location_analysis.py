#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Manage the analysis of a metavirom contig.

Usage:
    ./location_analysis.py <dir>

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
    print("\nAnalysing metavirome: "+args["<dir>"].split("/")[-2])
    list_contigs=[]
    list_sample=[]
    for sample in os.listdir(args["<dir>"]):
        if sample != "quast_results" and sample != "reads_on_contigs" :
            list_contigs.append(args["<dir>"]+sample+"/contigs.fasta")
            list_sample.append(sample)
            os.system("./metavirome_analysis.py "+args["<dir>"]+sample+"/")

    # Quast analyse
    if "quast_results" not in os.listdir(args["<dir>"]):
        os.system("./quast/quast.py "+" ".join(list_contigs)+" -o "+args["<dir>"]+
              "quast_results")
    else:
        print("\nQuast already used on this metavirome.")

    # Reads on contigs alignment
    print("\nReads alignement on contigs")
    # Check if the output dir exist
    if "reads_on_contigs" not in os.listdir(args["<dir>"]):
        os.system("mkdir "+args["<dir>"]+"reads_on_contigs")
    path_dir=args["<dir>"]+"reads_on_contigs/"
    # Contigs database creation
    if "contigs_database.fa" not in os.listdir(path_dir):
        print("Contigs database creation")
        os.system("./scripts/contigs_to_database.py "+args["<dir>"]+" -o "+
                  path_dir+"contigs_database.fa")
    else:
        print("Database already created")

    # Reads alignemnt on contigs using BWA.
    # Database indexation
    if "contigs_database.fa.amb" not in os.listdir(path_dir):
        print ("Database indexation")
        os.system("./bwa_kit/bwa index "+path_dir+"contigs_database.fa")
    else: 
        print("Database indexed")

    # Alignement:
    for sample in list_sample:
        if sample+".sam" not in os.listdir(path_dir):
            print("Aligning "+sample+" on contigs database")
            read = "data/"+args["<dir>"].split("/")[-2]+"/"+sample+".fa*"
            os.system("./bwa_kit/bwa aln "+path_dir+"contigs_database.fa "+read+
                      " > result.fai")
            os.system("./bwa_kit/bwa samse "+path_dir+"contigs_database.fa result.fai "+
                      read+" > "+path_dir+sample+".sam")
            os.system("rm result.fai")
        else:
            print(sample+" already aligned on contigs database")

##########
# LAUNCH #
##########
if __name__ == "__main__":
    args = docopt(__doc__, version="1.0")
    main(args)

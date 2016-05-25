#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Manage with SPAdes the genomic assembly of a read.

Usage:
    ./metavirome_assembly.py <read>

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
    path_read = os.path.abspath(args["<read>"]).split("/")
    name_metavirome = path_read[-2]
    name_read = path_read[-1].split(".")[0]
    if name_metavirome not in os.listdir("results"):
        os.makedirs("results/"+name_metavirome)
        os.makedirs("results/"+name_metavirome+"/"+name_read)
    if name_read not in os.listdir("results/"+name_metavirome):
        os.makedirs("results/"+name_metavirome+"/"+name_read)
    if "contigs.fasta" not in os.listdir("results/"+name_metavirome+"/"+name_read):
        os.system("./conf_assembly.sh "+args["<read>"]+" results/"+
                  name_metavirome+"/"+name_read)
        for res_file in os.listdir("results/"+name_metavirome+"/"+name_read):
            if res_file != "contigs.fasta":
                os.system("rm -rf results/"+name_metavirome+"/"+name_read+"/"+res_file)
    else:
        print("Job already done")

#############
# FUNCTIONS #
#############

##########
# LAUNCH #
##########
if __name__ == "__main__":
    args = docopt(__doc__, version="1.0")
    main(args)

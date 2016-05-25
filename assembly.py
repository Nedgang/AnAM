#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Manage, with SPAdes, the genomic assembly of all the data.

Usage:
    ./assembly.py

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
    for metavir in os.listdir("data"):
        os.system("./location_assembly.py data/"+metavir+"/")

##########
# LAUNCH #
##########
if __name__ == "__main__":
    args = docopt(__doc__, version="1.0")
    main(args)

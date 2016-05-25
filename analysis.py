#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Manage the analysis of all the data.

Usage:
    ./analysis.py

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
    for metavir in os.listdir("results"):
        os.system("./location_analysis.py results/"+metavir+"/")

##########
# LAUNCH #
##########
if __name__ == "__main__":
    args = docopt(__doc__, version="1.0")
    main(args)

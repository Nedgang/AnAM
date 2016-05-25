#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Manage, with SPAdes, the genomic assembly of a complete metavirome.

Usage:
    ./location_assembly.py <dir>

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
    for read in os.listdir(args["<dir>"]):
        os.system("./metavirome_assembly.py "+args["<dir>"]+read)

#############
# FUNCTIONS #
#############

##########
# LAUNCH #
##########
if __name__ == "__main__":
    args = docopt(__doc__, version="1.0")
    main(args)

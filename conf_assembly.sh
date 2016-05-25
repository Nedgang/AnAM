#!/bin/bash
# $1: initial reads
# $2: prefixe of results repository

# The SPAdes command you want to use to asseble you reads
./spades/bin/spades.py -k 21,33,55,77 --careful --12 $1 -o $2 --only-assembler -m 13

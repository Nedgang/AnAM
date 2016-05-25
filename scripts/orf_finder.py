#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Read a set of sequences and detect in it the ORFs.
Return a file containing all the ORFs, with some metadata.
This script use codon table from the NCBI, so check this link to choose which
one to use: http://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi<Paste>
By default, the threshold is at 100 (nt or aa), and the table used is the
bacterial and viral codon table (11). 

Usage:
    ./orf_finder.py <sequences> (--output=<file>) [options]

Options:
    --dna, -d               If you want ORF in nucleic version
    --format, -f=<string>   The files format [default: fasta]
    --help, -h              Display this screen.
    --output, -o=<file>     The name of the output file (erase if exist)
    --size, -s=<int>        Minimal ORF size accepted [default: 100]
    --table, -t=<int>       The ncbi codon table used [default: 11]
    --version,-v            The script version

"""

##########
# IMPORT #
##########
import os

from docopt import docopt
from Bio import SeqIO
from Bio.Data import CodonTable
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

########
# MAIN #
########
def main(args):
    """
    Just a regular main, which call all the differents functions, and do 
    barely nothing else (matters).
    """
    # First of all, extract the sequences.
    list_sequences = extract(args["<sequences>"], args["--format"])
    # ORF extraction.
    if args["--dna"]:
        list_orf = dna_orf_finder(list_sequences, args["--table"], args["--size"])
    else:
        list_orf = proteic_orf_finder(list_sequences, args["--table"], args["--size"])
    # Print the result into a file
    print_file(list_orf, args["--format"], args["--output"])

#############
# FUNCTIONS #
#############
def extract(path_file, file_format):
    """
    Extract all infos from the sequences file.
    """
    # A generator, juste because it's beautifull
    label_list = [sequence for sequence in
                  SeqIO.parse(os.path.abspath(path_file), file_format)]
    return label_list

def proteic_orf_finder(list_record, table, size):
    list_orf = []
    min_pro_len = int(size)
    for record in list_record:
        nb_orf = 0
        seq_len = len(record.seq)
        for strand, nuc in [(+1, record.seq), (-1, record.seq.reverse_complement())]:
            for frame in range(3):
                trans = str(nuc[frame:].translate(table))
                trans_len = len(trans)
                aa_start = 0
                aa_end = 0
                while aa_start < trans_len:
                    aa_end = trans.find("*", aa_start)
                    if aa_end == -1:
                        aa_end = trans_len
                    if aa_end-aa_start >= min_pro_len:
                        nb_orf += 1
                        if strand == 1:
                            start = frame+aa_start*3
                            end = min(seq_len,frame+aa_end*3+3)
                        else:
                            start = seq_len-frame-aa_end*3-3
                            end = seq_len-frame-aa_start*3
                        list_orf.append(SeqRecord(Seq(trans[aa_start:aa_end]),\
                                        id=record.id+"_ORF"+str(nb_orf),\
                                        name=record.id+"_ORF"+str(nb_orf),\
                                        description="nt:"+\
                                        str(start)+"-"+str(end)+" strand:"+\
                                        str(strand)))
                    aa_start = aa_end+1
    return list_orf

def dna_orf_finder(list_seq, table_num, size):
    list_orf  = []
    threshold = int(size)
    # Import of codon table
    codon_table = CodonTable.unambiguous_dna_by_id[int(table_num)]
    for seq in list_seq:
        num_orf  = 0
        # Normal strand
        for index in range(len(seq.seq)-2):
            triplet = seq.seq[index]+seq.seq[index+1]+seq.seq[index+2]
            # If we find a start codon:
            if triplet in codon_table.start_codons:
                num_orf += 1
                for ind in range(index, len(seq.seq)-2, 3):
                    triplet = seq.seq[ind]+seq.seq[ind+1]+seq.seq[ind+2]
                    if triplet in codon_table.stop_codons:
                        orf = SeqRecord(seq.seq[index:ind+3],\
                                        id=seq.id+" ORF"+str(num_orf),\
                                        name=seq.name,\
                                        description="coding_strand")
                        if len(orf.seq) > threshold:
                            list_orf.append(orf)
                        break
                    if ind == max(range(index, len(seq.seq)-2, 3)):
                        orf = SeqRecord(seq.seq[index:],\
                                        id=seq.id+" ORF"+str(num_orf),\
                                        name=seq.name,\
                                        description="coding_strand")
                        if len(orf.seq) > threshold:
                            list_orf.append(orf)
        # Reverse strand
        rev_seq = seq.seq.reverse_complement()
        for index in range(len(seq.seq)-2):
            triplet = rev_seq[index]+rev_seq[index+1]+rev_seq[index+2]
            # If we find a start codon:
            if triplet in codon_table.start_codons:
                num_orf += 1
                for ind in range(index, len(seq.seq)-2, 3):
                    triplet = rev_seq[ind]+rev_seq[ind+1]+rev_seq[ind+2]
                    if triplet in codon_table.stop_codons:
                        orf = SeqRecord(rev_seq[index:ind+3],\
                                        id=seq.id+" ORF"+str(num_orf),\
                                        name=seq.name,\
                                        description="reverse strand")
                        if len(orf.seq) > threshold:
                            list_orf.append(orf)
                        break
                    if ind == max(range(index, len(seq.seq)-2, 3)):
                        orf = SeqRecord(rev_seq[index:],\
                                        id=seq.id+" ORF"+str(num_orf),\
                                        name=seq.name,\
                                        description="reverse strand")
                        if len(orf.seq) > threshold:
                            list_orf.append(orf)
    return list_orf

def print_file(selected_seq, seq_type, output):
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
    args = docopt(__doc__, version="1.1")
    main(args)

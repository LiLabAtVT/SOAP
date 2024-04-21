#!/usr/bin/env python
"""
Description: Concat all the SNP files
This wasn't run for Ralstonia as no core genes were identified
Input directory: 
Output directory: 
Author: Sandeep Chinnareddy
Date: 01/20/2023
"""
# Concat SNP files based on ID match.
# Sandeep Chinnareddy
# 02/05/2023

from Bio import SeqIO
import sys


def concatenate_SNP(fasta1, fasta2):
    # Create a dictionary to store the sequences from first SNP file
    fasta1_dict = {}
    for record in SeqIO.parse(fasta1, "fasta"):
        fasta1_dict[record.id[0:13]] = str(record.seq)
    
    # Concatenate the sequences from the second FASTA file to the dictionary
    for record in SeqIO.parse(fasta2, "fasta"):
        if record.id[0:13] in fasta1_dict:
            fasta1_dict[record.id[0:13]] += str(record.seq)
        else:
            print(fasta2, " is not a core  gene")
    
    # Write the concatenated sequences to a new FASTA file
    with open("concatenated.fasta", 'w') as outfile:
        for id, seq in fasta1_dict.items():
            outfile.write(">" + id + "\n")
            outfile.write(seq + "\n")

            
def check_same_length(fasta_file):
    # Read the FASTA file and store the sequences in a dictionary
    sequences = {}
    with open(fasta_file) as f:
        current_seq = ""
        for line in f:
            if line.startswith(">"):
                if current_seq:
                    sequences[header] = current_seq
                    current_seq = ""
                header = line.strip()
            else:
                current_seq += line.strip()
        sequences[header] = current_seq
    
    # Check if all the sequences are the same length
    lengths = set(len(seq) for seq in sequences.values())
    if len(lengths) == 1:
        return True
    else:
        return False

    
files = sys.argv
input1 = files[1]
input2 = files[2]

print("The input files are", input1, input2)

if check_same_length(input1) and check_same_length(input1):
    concatenate_SNP(input1, input2)
    print("Done")
else:
    print("Length requirement not satsified", input1, input2)
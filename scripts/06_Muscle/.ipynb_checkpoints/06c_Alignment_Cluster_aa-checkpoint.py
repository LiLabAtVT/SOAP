"""
Description: Construct the dataset 1 (Presence Absence matrix).
Input directory: results/05_Presence_Absence
Output directory: results/05_Presence_Absence
Author: Sandeep Chinnareddy
Date: 01/20/2023
"""

# Alignment_Cluster_aa.py
# Prepare nucleotides sequences for each gene family using the mmseq output file

import xlrd
print(xlrd.__version__)
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_haxs_iter = True
from Bio import SeqIO
import pandas as pd
import os
from glob import glob

# change the following path to where the fna files are
path = 'data/allProdigal/results/modified_faa'
filename = "0.5_mmseqsFinal.xlsx"

# change the following path to where the MMSeq matrix file are
os.chdir('data/allProdigal/results/modified2/0.5')

book = xlrd.open_workbook(filename)
sheet = book.sheets()[0]

os.chdir(path)

for i in range(sheet.nrows):
    if i == 0:
        sample = sheet.row_values(0)
    else:
        for j in range(sheet.ncols):
            if j == 0:
                cluster = sheet.row_values(i)[0]
            elif j == 1 or j == 2 or j == 3:
                continue
            else:
                gene_mul = sheet.row_values(i)[j]
                gene = gene_mul.split()
                for k in gene:
                    print(i, cluster, sample[j], k)
                    files = glob('*{}*'.format(sample[j]))
                    for fasta_file in files:
                        fasta_sequences = SeqIO.parse(open(fasta_file), 'fasta')
                        os.chdir(path + '/assembled')
                        with open ("%s" % cluster + '.ffn', 'a') as f:
                            for seq in fasta_sequences:
                                if k == seq.id:
                                    SeqIO.write([seq], f, "fasta")
                        os.chdir(path)
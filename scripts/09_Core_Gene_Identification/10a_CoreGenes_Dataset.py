"""
Description:
This wasn't run for Ralstonia as no core genes were identified
Input directory: 
Output directory: 
Author: Sandeep Chinnareddy
Date: 01/20/2023
"""

## Read CSV file
import os
import pandas as pd


mmseq_matrix = pd.read_csv("0.5_mmseqsFinal.csv")

core_genes = []
for index, row in mmseq_matrix.iterrows():
    if row['#genes'] == 745 and row['#genomes'] == 745:
        core_genes.append(row[0])

import os

#TODO
core_path = ''


# Check if all the core genes have corresponding SNP files
gene_count = 0
cg_without_snp = []
for gene in core_genes:
    path = core_path
    path += gene + '_aa2nt_nogap_snp.fasta'
    if not os.path.isfile(path):
        gene_count += 1
        print(gene_count)
        cg_without_snp.append(gene)
        print(gene)

gene_count = 0
for gene in cg_without_snp:
    path = core_path
    path += gene + '_aa2nt_nogap.fasta'
    if not os.path.isfile(path):
        gene_count += 1

# Run the SNP Identifier for all the remaining Core genes
iter_count = 0
for gene in cg_without_snp:
    filename = gene + '_aa2nt_nogap.fasta'
    command = "python3 SNP_Identifier.py " + filename
    os.system(command)
    iter_count += 1

'''
In our studies, 7 files have not been generated, Proceeding to create dataset without the following 7 gene family files:

['GCA_001756025_CP074663.1_1025',
 'GCA_001756025_CP074663.1_1057',
 'GCA_001756025_CP074663.1_1249',
 'GCA_001756025_CP074663.1_1345',
 'GCA_001756025_CP074663.1_1441',
 'GCA_001756025_CP074663.1_1473',
 'GCA_001756025_CP074663.1_1505']
 
 We will be using the order of Core Genes to produce the final dataset in the form of a fasta file, we will concatenate each gene family at the end of another gene family
'''

# Move all the core gene files from pal2nal_results/nogap to pal2nal_results/nogap/core_genes
import shutil
os.chdir('/projects/leaph/sandeep/ncbi_dataset/data/pal2nal_results/nogap')
path = '/projects/leaph/sandeep/ncbi_dataset/data/pal2nal_results/nogap'
destination_path = '/projects/leaph/sandeep/ncbi_dataset/data/pal2nal_results/nogap/core_genes/'
gene_abs_count = 0
gene_count = 0
cg_without_snp = []
for gene in core_genes:
    path = '/projects/leaph/sandeep/ncbi_dataset/data/pal2nal_results/nogap/'
    path += gene + '_aa2nt_nogap.fasta'
    destination_path = '/projects/leaph/sandeep/ncbi_dataset/data/pal2nal_results/nogap/core_genes/'
    destination_path += gene + '_aa2nt_nogap.fasta'
    if not os.path.isfile(path):
        gene_count += 1
        print(gene_abs_count)
        cg_without_snp.append(gene)
        print(gene)
    else:
        shutil.copyfile(path, destination_path)
        gene_count += 1
        print(gene_abs_count)
        print('successfully copied ',gene)

# Let's remove the CG that couldn't create SNP from core_genes
cg_with_snp = [i for i in core_genes if i not in cg_without_snp]

# Function to Verify if all the ssequences in a FASTA file have the same sequence length
from Bio import SeqIO
import sys

def check_same_length(fasta_file):
    # Use SeqIO to parse the fasta file
    records = list(SeqIO.parse(fasta_file, "fasta"))
    # Get the length of the first sequence
    if(len(records) == 0): 
        return False
    first_seq_length = len(records[0].seq)
    # Loop through the remaining sequences and check if their length matches the first sequence
    for record in records[1:]:
        if len(record.seq) != first_seq_length:
            return False
    else:
        return True

# Function to get the length of sequence
def get_common_length(fasta_file):
    if check_same_length(fasta_file):
        # Use SeqIO to parse the fasta file
        records = list(SeqIO.parse(fasta_file, "fasta"))
        return len(records[0].seq)
    else:
        return 0


# Check if all the SNP files are satisfying length requirement
for count, gene in enumerate(cg_with_snp):
    path = '/projects/leaph/sandeep/ncbi_dataset/data/pal2nal_results/nogap/core_genes/cg_snp/'
    path += gene + '_aa2nt_nogap_snp.fasta'
    if not check_same_length(path):
        print(gene)

# Loop to concatenate all the 2519 genes
for count, gene in enumerate(cg_with_snp):
    if count>1:
        filename = gene + '_aa2nt_nogap_snp.fasta'
        command = "python3 SNP_Concat.py concatenated.fasta " + filename
        os.system(command)
        print(count,filename)

#Write individual gene family length - it becomes simpler to find which gene positions are from which fene family
def get_common_length(fasta_file):
    if check_same_length(fasta_file):
        # Use SeqIO to parse the fasta file
        records = list(SeqIO.parse(fasta_file, "fasta"))
        return len(records[0].seq)
    else:
        return 0

SNP_lengths = dict()
for gene in cg_with_snp:
    fasta_file = core_path + '/cg_snp'
    fasta_file += gene + '_aa2nt_nogap_snp.fasta' 
    SNP_lengths[gene] = get_common_length(fasta_file)


# Export these lengths to a CSV
import csv

my_dict = SNP_lengths
output_file = "/dataset_gene_lengths.csv"
# Open the CSV file for writing

# Open the CSV file for writing
with open(output_file, 'w', newline='') as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)

    # Write the header row to the CSV file
    writer.writerow(['Gene Name', 'Lengths'])

    # Write each key-value pair to the CSV file
    for gene_name, distance in SNP_lengths.items():
        writer.writerow([gene_name, distance])

import csv
from Bio import SeqIO

# Specify the path to your fasta file and the output csv file
fasta_file = core_path + "/cg_snp/concatenated.fasta"
csv_file = core_path + "/cg_snp/dataset.csv"

with open(csv_file, 'w', newline='') as csv_output:
    csv_writer = csv.writer(csv_output)
    csv_writer.writerow(['id', 'sequence'])
    records = SeqIO.parse(fasta_file, 'fasta')
    for record in records:
        csv_writer.writerow([record.id, str(record.seq)])


# Code to Find source of a genome using the original Salmonella Excel data
# 02/20/2023

import openpyxl
from Bio import SeqIO

# open the FASTA file

data_file = "/Salmonella_THY_sources_2021.xlsx"
filename = fasta_file
final_fasta_file = open(filename, "r")

# create an empty list to store the headers
headers = []
for record in SeqIO.parse(final_fasta_file, "fasta"):
    headers.append(record.description)
final_fasta_file.close()

# Open Source data file 
workbook = openpyxl.load_workbook(data_file)
worksheet = workbook.active

# dictionary to store the results
source_dictionary = {}

# loop through all rows in the Assembly Column
for row in worksheet.iter_rows(min_row=1, max_row=795, values_only=True):
    # check if the cell in Assembly Column contains any of the target strings
    # Assembly column index = 14
    # Source column index = 8
    for string in headers:
        
        if string != None and row[14] != None and string in row[14]:
        # if the string is found, store the value in Column B for the same row
            source_dictionary[string] = row[8]


import csv
from Bio import SeqIO

# input and output filenames
output_file = core_path + "/cg_snp/dataset2.csv"

length = get_common_length(fasta_file)

# open the output file for writing
with open(output_file, "w", newline="") as out:

    writer = csv.writer(out)
    writer.writerow(["Pos" + str(i) for i in range(1, length + 1)] + ["target"])

    for record in SeqIO.parse(fasta_file, "fasta"):
        # write the ID and sequence to the output file as a row
        row = [record.id] + list(str(record.seq)) + [source_dictionary.get(record.description)]
        writer.writerow(row)

# This completes Dataset Preperation

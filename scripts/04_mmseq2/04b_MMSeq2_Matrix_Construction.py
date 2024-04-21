"""
Description: Construct the final MMSeq matrix from the tsv file generated from the software.
Input directory: results/04_mmseq2
Output directory: results/04_mmseq2
Author: Sandeep Chinnareddy
Date: 01/20/2023
"""

#import libraries
from collections import defaultdict
from collections import OrderedDict
import glob
import pandas as pd 
import numpy as np
import csv
from openpyxl import Workbook
import os
import xlrd
print(xlrd.__version__) # Ensure the xlrd package version is 1.2
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True
from Bio import SeqIO
import pandas as pd
import os
from glob import glob

#TODO
path = "FILE_PATH_HERE"

data_list = []
with open("0.5.tsv", newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        data_list.append(row)
    d = defaultdict(list)
    for k, v in data_list:
        d[k].append(v)

d_order = OrderedDict(d)
ws = pd.DataFrame(index=np.arange(len(d_order)), columns=np.arange(750))
ws.fillna('', inplace=True)

# Create Genome file: a list of all the genome present in our data
genome = []
for x in os.listdir(path):
    if x.endswith(".faa"):
        genome.append(x[0:13])

n = 0;
ws = pd.DataFrame(index=np.arange(len(d_order)), columns=np.arange(750))
ws.fillna('', inplace=True)
for cluster, gene in d_order.items():
        ws.at[n, 0] = cluster[:]
        ws.at[n, 1] = len(gene)
        unique_list = []
        for i in gene:
            meg = i[0:13]
            index = genome.index(meg)
            index = int(index)
            ws.at[n, index + 4] = str(ws.at[n, index + 4]) + str(i[:]) + ' '
            if meg not in unique_list: 
                unique_list.append(meg)
        ws.at[n, 2] = len(unique_list)
        if(ws.at[n, 2] == ws.at[n,1]): ws.at[n,3] = False
        else: ws.at[n,3] = True
        n = n + 1


# add header row to table
header_list = ['', '#genes', '#genomes', 'if paralogs']
for assembly in genome:
    header_list.append(assembly)
header_list.append('')
ws.columns = header_list

ws.to_csv("0.5_mmseqsFinal.csv", index=False, header=True)
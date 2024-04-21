"""
Description: Construct the dataset 1 (Presence Absence matrix).
Input directory: results/04_mmseq2
Output directory: results/05_Presence_Absence
Author: Sandeep Chinnareddy
Date: 01/20/2023
"""

import os
import csv
import pandas as pd
import numpy as np
from collections import defaultdict, OrderedDict
from glob import glob

# Define constants for paths
INPUT_DIRECTORY = "results/04_mmseq2"
OUTPUT_DIRECTORY = "results/05_Presence_Absence"

def load_data(file_path):
    """ Load data from TSV file and return as defaultdict of lists. """
    data_list = []
    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for row in spamreader:
            data_list.append(row)
    data_dict = defaultdict(list)
    for k, v in data_list:
        data_dict[k].append(v)
    return OrderedDict(data_dict)

def create_presence_absence_matrix(data_order, genome_list):
    """ Create and return a presence-absence matrix as a DataFrame. """
    ws = pd.DataFrame(index=np.arange(len(data_order)), columns=np.arange(len(genome_list) + 4))
    ws.fillna('', inplace=True)
    header_list = ['', '#genes', '#genomes', 'if paralogs'] + genome_list
    ws.columns = header_list

    for idx, (cluster, genes) in enumerate(data_order.items()):
        ws.loc[idx, ''] = cluster
        ws.loc[idx, '#genes'] = len(genes)
        unique_genomes = list(set(g[:13] for g in genes))
        ws.loc[idx, '#genomes'] = len(unique_genomes)
        ws.loc[idx, 'if paralogs'] = len(unique_genomes) != len(genes)
        for gene in genes:
            genome_id = gene[:13]
            genome_index = genome_list.index(genome_id)
            ws.loc[idx, genome_id] += gene + ' '

    # Convert gene list entries to binary presence (1) or absence (0)
    for idx in range(ws.shape[0]):
        for genome in genome_list:
            ws.loc[idx, genome] = 1 if ws.loc[idx, genome] else 0

    return ws

def main():
    genome_list = [filename[:13] for filename in os.listdir(INPUT_DIRECTORY) if filename.endswith(".faa")]

    data_order = load_data(os.path.join(INPUT_DIRECTORY, "0.5.tsv"))
    pa_matrix = create_presence_absence_matrix(data_order, genome_list)
    pa_matrix.to_csv(os.path.join(OUTPUT_DIRECTORY, "0.5_mmseqs_Final_pre_abs.csv"), index=False, header=True)

if __name__ == "__main__":
    main()


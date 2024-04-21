"""
Description: Construct the dataset 1 (Presence Absence matrix).
Input directory: results/04_mmseq2
Output directory: results/05_Presence_Absence
Author: Sandeep Chinnareddy
Date: 01/20/2023
"""

# Alignment_Cluster_aa.py
# Prepare nucleotides sequences for each gene family using the mmseq output file

import pandas as pd
from Bio import SeqIO
import os
from glob import glob

# Define paths
nucleotides_dir = '/data/assembly_data'
results_dir = '/results/05_mmseq2/0.5'
assembled_dir = os.path.join(nucleotides_dir, 'assembled')
filename = "0.5_mmseqsFinal.xlsx"

# Create the assembled directory if it doesn't exist
os.makedirs(assembled_dir, exist_ok=True)

# Load the Excel file using pandas
df = pd.read_excel(os.path.join(results_dir, filename), sheet_name=0)

# Get the header names (samples)
samples = df.columns.tolist()

# Process each row in the DataFrame after the header
for idx, row in df.iterrows():
    if idx == 0:
        continue  # Skip header row, already handled
    cluster = row[0]  # First column is cluster ID
    for col_idx, gene_mul in enumerate(row[4:], start=4):  # Skip the first three metadata columns
        if pd.notna(gene_mul):
            genes = gene_mul.split()
            sample_id = samples[col_idx]
            pattern = f"*{sample_id}*"
            files = glob(os.path.join(nucleotides_dir, pattern))
            for fasta_file in files:
                fasta_sequences = SeqIO.parse(open(fasta_file), 'fasta')
                output_path = os.path.join(assembled_dir, f"{cluster}.ffn")
                with open(output_path, 'a') as f:
                    for seq in fasta_sequences:
                        if seq.id in genes:
                            SeqIO.write([seq], f, "fasta")

print("Processing complete.")

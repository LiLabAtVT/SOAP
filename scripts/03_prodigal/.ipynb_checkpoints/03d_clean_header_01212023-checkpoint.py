#!/usr/bin/env python

"""
Description: Clean and rename sequence IDs in .ffn files, appending the filename as a prefix to each sequence ID.
Input directory: /projects/leaph/sandeep/Sandeep_SourceAttributionPipeline_2023/data/assembly_data/
Output directory: /projects/leaph/sandeep/Sandeep_SourceAttributionPipeline_2023/data/allProdigal/results/modified2/
Author: Sandeep Chinnareddy
Date: 01/20/2023
"""

import glob
import os
from Bio import SeqIO

# Define input and output directories
input_dir = ""
output_dir = ""

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Change to the input directory
os.chdir(input_dir)

# Process each .ffn file in the input directory
for fname in glob.glob("*.ffn"):
    # Parse each sequence in the .ffn file
    for seq_record in SeqIO.parse(fname, "fasta"):
        # Rename the sequence ID
        seq_record.id = fname[:-4] + " " + seq_record.id
        
        # Change to the output directory to write the modified sequence
        with open(os.path.join(output_dir, fname[:-4] + "_clean.faa"), "a") as handle:
            SeqIO.write(seq_record, handle, "fasta")
    
    print(f"Completed cleaning {fname}")

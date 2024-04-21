#!/bin/bash

# Description: Download genomic data from ncbi website, using the Assembly IDs in Genome_List.txt 
# working directory: /projects/leaph/sandeep/Sandeep_SourceAttributionPipeline_2023/
# input files: raw_data/Genome_List.txt
# output directory: data/assembly_data
# Author: Sandeep Chinnareddy
# Date: 11/05/2023

#SBATCH -J Data_download # job name
#SBATCH --account= ENTER_ACCOUNT
#SBATCH --partition=normal_q
#SBATCH --time=1-00:00:00 # 10 minutes; format: days-hours:minutes:seconds
#SBATCH --mem=128G # based on memory used when testing with interactive jobs
#SBATCH --mail-user= EMAIL #enter desired email address for updates
#SBATCH --mail-type=BEGIN #include to get emailed when job begins
#SBATCH --mail-type=END #include to get emailed when job ends
#SBATCH --mail-type=FAIL #include to get emailed if job fails

# Define the file containing the list of accession codes
ACCESSION_FILE="/rawdata/metadata/Genome_List.txt"
DOWNLOAD_DIR="/data/assembly_data"

mkdir -p "$DOWNLOAD_DIR"

while IFS= read -r accession; do
    echo "Downloading genomic data for accession: $accession"
    # Use the datasets command to download the data
    ncbi datasets download genome accession "$accession" --output "$DOWNLOAD_DIR/$accession.zip"
done < "$ACCESSION_FILE"

echo "Download completed."

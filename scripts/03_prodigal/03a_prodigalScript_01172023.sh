#!/bin/bash

# Description: Perform PRODIGAL analysis on the genomic data downloaded from NCBI 
# working directory: /projects/leaph/sandeep/Sandeep_SourceAttributionPipeline_2023/
# input root directory: /data/assembly_data
# output : results/03_prodigal
# Author: Sandeep Chinnareddy
# Date: 01/17/2023

#SBATCH -J PRODIGAL # job name
#SBATCH --account=
#SBATCH --partition=normal_q
#SBATCH --time=1-00:00:00 # 1 day; format: days-hours:minutes:seconds
#SBATCH --mem=128G # based on memory used when testing with interactive jobs
#SBATCH --mail-user= #enter desired email address for updates
#SBATCH --mail-type=BEGIN #include to get emailed when job begins
#SBATCH --mail-type=END #include to get emailed when job ends
#SBATCH --mail-type=FAIL #include to get emailed if job fails

# Define the working directory, input root directory, and output directory
WORKING_DIR=""
INPUT_ROOT_DIR="${WORKING_DIR}/data/assembly_data"
OUTPUT_DIR="${WORKING_DIR}/results/03_prodigal"

# Ensure the output directory and input directory exists
mkdir -p "$OUTPUT_DIR"
cd "$INPUT_ROOT_DIR" || exit

# # More info: https://www.docs.arc.vt.edu/usage/slurm.html
# source activate base # activate env if necessary

function prodigal_loop {
    for f in *; do
        if [ -d "$f" ] && [ ! -h "$f" ]; then
            cd -- "$f" || continue
            echo "Performing Prodigal Analysis in $(pwd)/$f"
            for filename in *.fna; do
                PRODIGAL_OUTPUT_SUBDIR="${OUTPUT_DIR}/${f}"
                mkdir -p "$PRODIGAL_OUTPUT_SUBDIR"

                # Run Prodigal and direct output files to the corresponding output subdirectory
                prodigal -i "$filename" -a "${PRODIGAL_OUTPUT_SUBDIR}/${filename%.fna}.faa" \
                         -d "${PRODIGAL_OUTPUT_SUBDIR}/${filename%.fna}.ffn" -f gbk \
                         -o "${PRODIGAL_OUTPUT_SUBDIR}/${filename%.fna}.gbk" -s "${PRODIGAL_OUTPUT_SUBDIR}/${filename%.fna}.txt"
            done

            # Return to the input root directory before processing the next directory
            cd "$INPUT_ROOT_DIR" || exit
        fi
    done
}

prodigal_loop


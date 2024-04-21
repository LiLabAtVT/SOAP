#!/bin/bash

# Description: Accumulate all .ffn files from PRODIGAL analysis into a single directory 
# working directory: /projects/leaph/sandeep/Sandeep_SourceAttributionPipeline_2023/
# input root directory: data/assembly_data/
# output directory: data/allProdigal/nucleotides/
# Author: Sandeep Chinnareddy
# Date: 01/17/2023

#SBATCH -J ACCUMULATE_GENOMES # job name
#SBATCH --account=
#SBATCH --partition=normal_q
#SBATCH --time=00-12:00:00 # 12 hours; format: days-hours:minutes:seconds
#SBATCH --mem=64G # Adjust based on memory needs
#SBATCH --mail-user=#enter desired email address for updates
#SBATCH --mail-type=BEGIN #include to get emailed when job begins
#SBATCH --mail-type=END #include to get emailed when job ends
#SBATCH --mail-type=FAIL #include to get emailed if job fails

# Define the working directory, input root directory, and output directory
WORKING_DIR=""
INPUT_ROOT_DIR="${WORKING_DIR}/results/03_prodigal"
OUTPUT_DIR="${WORKING_DIR}/results/03_prodigal/nucleotides"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"
cd "$INPUT_ROOT_DIR" || exit

echo "Starting accumulation of .ffn files to ${OUTPUT_DIR}"

# Accumulate all .ffn genome files to a single directory called allGenome
for f in *; do
    if [ -d "$f" ] && [ ! -h "$f" ]; then
        cd -- "$f" || continue
        for filename in *.ffn; do
            # Make a copy of the file to the output directory
            cp "$filename" "${OUTPUT_DIR}/${f}_${filename}"
            echo "Completed making a copy of $filename from $f Prodigal Result"
            break # Stops after the first .ffn file; remove if all .ffn files should be copied
        done
        cd "$INPUT_ROOT_DIR" || exit
    fi
done

echo "Accumulation of .ffn files completed."

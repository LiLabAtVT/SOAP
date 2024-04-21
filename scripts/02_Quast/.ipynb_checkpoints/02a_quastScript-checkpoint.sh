#!/bin/bash

# Description: Performs QUAST analysis on a list of genome sequences 
# working directory: /projects/leaph/sandeep/Sandeep_SourceAttributionPipeline_2023/
# input files: data/assembly_data
# output directory: results/02_QUAST
# Author: Sandeep Chinnareddy
# Date: 01/04/2023

#SBATCH -J quast-function
#SBATCH --account= ENTER ACCOUNT
#SBATCH --partition=normal_q
#SBATCH --time=1-00:00:00 # 10 minutes; format: days-hours:minutes:seconds
#SBATCH --mem=128G # based on memory used when testing with interactive jobs
#SBATCH --mail-user= EMAIL #enter desired email address for updates
#SBATCH --mail-type=BEGIN #include to get emailed when job begins
#SBATCH --mail-type=END #include to get emailed when job ends
#SBATCH --mail-type=FAIL #include to get emailed if job fails

# Directories setup
INPUT_DIRECTORY="data/assembly_data"
OUTPUT_DIRECTORY="results/02_QUAST"
QUAST_EXECUTABLE="/projects/leaph/pyenv/versions/mambaforge/bin/quast.py"

# Recursive function to handle directories
function process_directory() {
    local current_directory=$1
    echo "Entering directory: $current_directory"
    cd "$current_directory" || exit 1

    for item in *; do
        if [ -d "$item" ] && [ ! -h "$item" ]; then
            echo "Performing Quast Analysis in $PWD/$item"
            # Recursively process subdirectories
            process_directory "$PWD/$item"
        elif [[ "$item" == *.fna ]]; then
            # Perform Quast on .fna files
            mkdir -p "${OUTPUT_DIRECTORY}/${current_directory}"
            $QUAST_EXECUTABLE -o "${OUTPUT_DIRECTORY}/${current_directory}/quast_report" "$item"
            echo "Quast analysis completed for $item"
        fi
    done

    cd ..
}

# Start the script from the base input directory
cd "$INPUT_DIRECTORY" || exit 1
process_directory "$PWD"


#!/bin/bash

# Description: accumulating all the genome files to a single directory called allGenome
# working directory: /projects/leaph/sandeep/Sandeep_SourceAttributionPipeline_2023/
# input root directory: data/assembly_data/
# output directory: data/allProdigal/nucleotides/
# Author: Sandeep Chinnareddy
# Date: 01/17/2023

#SBATCH -J quast-function
#SBATCH --account= ENTER ACCOUNT
#SBATCH --partition=normal_q
#SBATCH --time=1-00:00:00 # 10 minutes; format: days-hours:minutes:seconds
#SBATCH --mem=128G # based on memory used when testing with interactive jobs
#SBATCH --mail-user= EMAIL #enter desired email address for updates
#SBATCH --mail-type=BEGIN #include to get emailed when job begins
#SBATCH --mail-type=END #include to get emailed when job ends
#SBATCH --mail-type=FAIL #include to get emailed if job fails

#!/bin/bash

# Set the base working directory
BASE_DIR="/projects/leaph/sandeep/Sandeep_SourceAttributionPipeline_2023"

# Input root directory containing genome files
INPUT_DIR="${BASE_DIR}/data/assembly_data"

# Output directory for accumulated genome files
OUTPUT_DIR="${BASE_DIR}/data/allProdigal/nucleotides"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Find and copy all *.fna files to the output directory
find "$INPUT_DIR" -type f -name "*.fna" -exec sh -c '
    for fna_file do
        # Extract filename and directory name for renaming
        file_name=$(basename "$fna_file")
        dir_name=$(basename "$(dirname "$fna_file")")
        
        # Construct new filename and copy path
        new_file="${dir_name}_${file_name}"
        dest_path="${OUTPUT_DIR}/${new_file}"
        
        # Copy and rename the file
        cp "$fna_file" "$dest_path"
        echo "Completed making a copy of $fna_file to $dest_path"
    done
' sh {} +


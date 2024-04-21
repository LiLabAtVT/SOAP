#!/bin/bash

# Description: alignment multiple multi-fasta files using muscle
# working directory: /projects/leaph/sandeep/Sandeep_SourceAttributionPipeline_2023/
# input files: results/
# output directory: data/assembly_data
# Author: Sandeep Chinnareddy
# Date: 07/06/2023

#SBATCH -J quast-function
#SBATCH --account= ENTER ACCOUNT
#SBATCH --partition=normal_q
#SBATCH --time=1-00:00:00 # 10 minutes; format: days-hours:minutes:seconds
#SBATCH --mem=128G # based on memory used when testing with interactive jobs
#SBATCH --mail-user= EMAIL #enter desired email address for updates
#SBATCH --mail-type=BEGIN #include to get emailed when job begins
#SBATCH --mail-type=END #include to get emailed when job ends
#SBATCH --mail-type=FAIL #include to get emailed if job fails

# Add MUSCLE to the PATH
export PATH="/programs/muscle3.8.31:$PATH"

# Directory for results
RESULTS_DIR="muscle_results"
LOG_DIR="logfile"
ALIGN_DIR="aligned"

# Create directories if they do not exist
mkdir -p "$RESULTS_DIR" "$LOG_DIR" "$ALIGN_DIR"

# Loop over all .faa files in the current directory
for f in *.faa; do
    base_name="${f%.faa}"
    alignment_file="${RESULTS_DIR}/${base_name}_align.faa"
    log_file="${LOG_DIR}/log_${base_name}.txt"

    # Check if the alignment file already exists
    if [[ -f "$alignment_file" ]]; then
        echo "File already exists: $alignment_file"
    else
        # Perform MUSCLE alignment and capture the output to a log file
        muscle -super5 "$f" -output "$alignment_file" |& tee "$log_file"
    fi
done

# Move alignment files to the aligned directory
mv ${RESULTS_DIR}/*_align.faa "$ALIGN_DIR"


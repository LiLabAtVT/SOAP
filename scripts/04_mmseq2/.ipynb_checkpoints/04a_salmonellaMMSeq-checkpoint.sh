#!/bin/bash

# Description: Performs MMSeq2 analysis on the concatenated list
# working directory: /projects/leaph/sandeep/Sandeep_SourceAttributionPipeline_2023/
# input files: results/03_Prodigal
# output directory: results/04_mmseq2
# Author: Sandeep Chinnareddy
# Date: 01/04/2023

#SBATCH -N 1
#SBATCH -c 20
#SBATCH -t 10:00:00
#SBATCH -p sched_mit_chisholm
#SBATCH --mem=10G
#SBATCH -J salmonella-prodigal-mmseq # job name
#SBATCH --account = 
#SBATCH --partition = 


export PATH=/programs/mmseqs/bin:$PATH
​
min_id=0.5
BASE_DIR="" # /projects/leaph/sandeep/ncbi_dataset/data/allProdigal/results/modified2
DBPATH="" # /projects/leaph/sandeep/ncbi_dataset/data/allProdigal/results/modified2/toClust
cd "$BASE_DIR"
​
if [ ! -f $DBPATH ]; then
	INDB="/projects/leaph/sandeep/ncbi_dataset/data/allProdigal/results/modified2/prodigal_final.fna"
	mmseqs createdb $INDB $DBPATH
fi
​
mkdir "$min_id"
cd "$min_id"
​
# clusters need to align to 80% of longest sequence with minimum of
# 30% sequence identity
mmseqs cluster \
	$DBPATH \
	"$min_id" \
	tmp \
	--cov-mode 1\
	--min-seq-id $min_id \
	-c 0.8 \
	--threads 15 \
	--max-seqs 10000
​
mmseqs createtsv \
	$DBPATH \
	$DBPATH \
	"$min_id" \
	"$min_id.tsv"
​
rm -rf tmp

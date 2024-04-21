#!/bin/bash

# Description: accumulating all the quast report files to a single directory called quast analysis
# working directory: /projects/leaph/sandeep/Sandeep_SourceAttributionPipeline_2023/
# input files: results/02_QUAST
# output directory: results/02_QUAST
# Author: Sandeep Chinnareddy
# Date: 02/06/2023

#SBATCH -J quast-function
#SBATCH --account= ENTER ACCOUNT
#SBATCH --partition=normal_q
#SBATCH --time=1-00:00:00 # 10 minutes; format: days-hours:minutes:seconds
#SBATCH --mem=128G # based on memory used when testing with interactive jobs
#SBATCH --mail-user= EMAIL #enter desired email address for updates
#SBATCH --mail-type=BEGIN #include to get emailed when job begins
#SBATCH --mail-type=END #include to get emailed when job ends
#SBATCH --mail-type=FAIL #include to get emailed if job fails

for f in *;  
    do
    if [ -d $f  -a ! -h $f ];
        then
            cd -- "$f";

            for folder2 in * 
                do
                if [ -d $folder2  -a ! -h $folder2 ]; 
                     then
                         cd -- "$folder2";
                         for filename in *.txt
                             do
                             if [ "${filename}" == "report.txt" ]
                             then
                                  # make a copy of the file
                                  # rename the file
                                  # copy the file to directory
                                  cp $filename /projects/leaph/sandeep/ncbi_dataset/data/quast_reports/$f.txt
                                  echo "Completed making a copy of $f quast report";
                                  break
                             fi;
                             done;

                cd ..;
                fi;
            done;
            cd ..;

    fi;
done;

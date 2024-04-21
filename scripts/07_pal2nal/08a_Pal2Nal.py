"""
Description: Run PAL2NAL. This code was not run for Ralstonia data as no core genes were constructed
Author: Sandeep Chinnareddy
Date: 01/20/2023
"""

import glob
import sys
import subprocess
import datetime
import os
import time

import os
os.chdir('')

!mkdir pal2nal

#copy aligned AA to pal2nal documentary
!cp aligned/* pal2nal/

#copy nucleotides to pal2nal documentary
!cp nucleotides/* pal2nal/

#copy source code to pal2nal documentary
!cp pal2nal.pl pal2nal/

#copy Loop wrapper code to pal2nal documentary
!cp PAL2NAL_loop.pl pal2nal/

# AMINO ACID FILES WITH NO GAP
for fname in glob.glob("*_align.faa"):
    nt = fname[:-10] + ".ffn"
    command = ["perl", "pal2nal.pl", fname, nt, "-output", "fasta", "-nogap"]
    with open(fname[:-10] + "_aa2nt_nogap.fasta", 'wb', 0) as out:
        subprocess.call(command, stdout=out)

# AMINO ACID FILES WITH GAP
for fname_ in glob.glob("*_align.faa"):
    nt_ = fname_[:-10] + ".ffn"
    command_ = ["perl", "pal2nal.pl", fname_, nt_, "-output", "fasta"]
    with open(fname_[:-10] + "_aa2nt_withgap.fasta", 'wb', 0) as out_:
        subprocess.call(command_, stdout=out_) 
#!/usr/bin/env python

"""
Description: robust conversion of protein sequence alignments into the corresponding codon-based DNA alignments in a loop
This code was not run for Ralstonia data as no core genes were constructed
Author: Sandeep Chinnareddy
Date: 01/25/2023
"""

import glob
import sys
import subprocess
import datetime
import os
import time

for fname in glob.glob("*_align.faa"):
    nt = fname[:-10] + ".ffn"
    command = ["perl", "pal2nal.pl", fname, nt, "-output", "fasta", "-nogap"]
    with open(fname[:-10] + "_aa2nt_nogap.fasta", 'wb', 0) as out:
        subprocess.call(command, stdout=out)

for fname_ in glob.glob("*_align.faa"):
    nt_ = fname_[:-10] + ".ffn"
    command_ = ["perl", "pal2nal.pl", fname_, nt_, "-output", "fasta"]
    with open(fname_[:-10] + "_aa2nt_withgap.fasta", 'wb', 0) as out_:
        subprocess.call(command_, stdout=out_)       
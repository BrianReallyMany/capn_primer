#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import os
from src.dependency_checker import primer3_core_is_installed, blastall_is_installed
from src.fasta_reader import FastaReader
from src.gff_reader import GFFReader

## DEPENDENCIES: primer3_core, blast (?)
## input: fasta containing mrna_ids and CDS 
##        gff for genome from which fasta is pulled

def main():
    print("Yarr! I be Cap'n Primer.\n")
    # Check dependencies
    print("Ahoy, let's check these scurvy dependencies...")
    check_dependencies()

    # Verify files
    print("Yarr! Now to verify the input files...")
    target_fasta_path = 'targets.fasta'
    genome_fasta_path = 'genome.fasta'
    gff_path = 'genome.gff'
    options_path = 'primer3_options'

    for path in [target_fasta_path, genome_fasta_path, gff_path, options_path]:
        verify_path(path)

    print("Shiver me timbers, the input files be present. Now I'll be reading them...")

    # Read files
    fasta_reader = FastaReader()
    with open(target_fasta_path, 'rb') as target_file:
        target_seqs = fasta_reader.read(target_file)
    if not target_seqs:
        print("Yarr! Error reading target fasta. Walk the plank.")
        sys.exit()

    gff_reader = GFFReader()
    with open(gff_path, 'rb') as gff_file:
        gff_reader.read(gff_file)
    if not gff_reader.cds_segment_lengths:
        print("Yarr! Error reading GFF! Walk the plank.")
        sys.exit()

    primer3_options = ""
    with open(options_path, 'rb') as options_file:
        for line in options_file:
            primer3_options += line

    print("got " + str(len(target_seqs)) + " target seqs.")
    print("got " + str(len(gff_reader.cds_segment_lengths)) + " mrnas")

    # Prepare input for primer3_core
    boulder_formatter = BoulderIOFormatter()
    boulder_formatter.segment_lengths = gff_reader.cds_segment_lengths
    with open("target_seqs.boulder-io", "wb") as boulderfile:
        # write config data first
        boulderfile.write(primer3_options)
        for seq in target_seqs:
            boulderfile.write(boulder_formatter.format_seq(seq))

    # Run primer3_core

    # BLAST PRIMER SEQUENCES AGAINST GENOME TO MAKE SURE THEY ONLY AMPLIFY ONE REGION
        # concatenate left primer with reverse complement of right primer
        # make fasta
        # blastall against in-species genome (i guess) 
        # using e-value and alignment length cutoffs, discard matches you don't believe
        # each primer should have only one legit match. if it's got more than one, it's trasssh

        

def check_dependencies():
    # check primer3_core
    if primer3_core_is_installed():
        print("...Yarr! primer3_core be installed.")
    else:
        print("Yarr! Why ye not install primer3_core, scurvy dog.")
        sys.exit()

    # check blastall
    if blastall_is_installed():
        print("...Yarr! blastall be installed.\n")
    else:
        print("Yarr! Why ye not install blastall, scurvy dog.")
        sys.exit()

def verify_path(path):
    if not os.path.isfile(path):
        sys.stderr.write("Failed to find " + path + ". Walk the plank.\n")
        sys.exit()

if __name__ == '__main__':
    main()

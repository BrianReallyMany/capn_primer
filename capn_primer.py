#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import os
from src.dependency_checker import primer3_core_is_installed, blastall_is_installed
from src.fasta_reader import FastaReader
from src.gff_reader import GFFReader

## DEPENDENCIES: primer3_core, blast (?)
## data: fasta containing gene_ids and CDS 
##       gff for genome from which fasta is pulled
##       list of gene_ids to target

## maybe work backwards -- given fasta file of sequences to create primers for, run primer3_core and then blast against reference to verify.
## then can add in previous exploration steps.

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

    for path in [target_fasta_path, genome_fasta_path, gff_path]:
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


    # GIVEN: LIST OF GENE_IDS TO TARGET
    # GIVEN: FASTA WITH CDS FROM GENES OF INTEREST
    # GIVEN: GFF FOR GENOME IN QUESTION

    # make primer_settings.conf entry

    # FOR CDS IN FASTA:
        # make .boulder-io entry
        # from gff, obtain lengths of each CDS region from each gene
        # add SEQUENCE_TARGET attribute with one list/length pair for each intron junction 

    # RUN PRIMER3_CORE

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

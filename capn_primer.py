#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
from src.dependency_checker import primer3_core_is_installed, blastall_is_installed

## DEPENDENCIES: primer3_core, blast (?)
## data: fasta containing gene_ids and CDS 
##       gff for genome from which fasta is pulled
##       list of gene_ids to target

## maybe work backwards -- given fasta file of sequences to create primers for, run primer3_core and then blast against reference to verify.
## then can add in previous exploration steps.

def main():
    print("Yarr! I be Cap'n Primer.")
    print("Ahoy, let's check these scurvy dependencies...")

    check_dependencies()

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
        print("Yarr! primer3_core be installed.")
    else:
        print("Yarr! Why ye not install primer3_core, scurvy dog.")
        sys.exit()

    # check blastall
    if blastall_is_installed():
        print("Yarr! blastall be installed.")
    else:
        print("Yarr! Why ye not install blastall, scurvy dog.")
        sys.exit()


if __name__ == '__main__':
    main()

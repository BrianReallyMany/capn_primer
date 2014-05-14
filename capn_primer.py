#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import subprocess
import os
from src.dependency_checker import primer3_core_is_installed, blastall_is_installed
from src.fasta_reader import FastaReader
from src.gff_reader import GFFReader
from src.boulder_io_formatter import BoulderIOFormatter
from src.boulder_io_reader import BoulderIOReader

## DEPENDENCIES: primer3_core, blast (?)
## input: fasta containing mrna_ids and CDS 
##        gff for genome from which fasta is pulled

# TODO primers should not overlap at all with the primers from the last run. wtf
# so ... need to pass in a list of forbidden zones to primer3_core, or something.

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
    excluded_primers_path = 'primers_to_exclude.boulder-io'
    options_path = 'primer3_options'

    for path in [target_fasta_path, genome_fasta_path, gff_path, excluded_primers_path, options_path]:
        verify_path(path)

    print("Shiver me timbers, the input files be present. Now I'll be reading them...")

    # Read files
    print("Reading the scurvy " + target_fasta_path + " file...")
    fasta_reader = FastaReader()
    with open(target_fasta_path, 'rb') as target_file:
        target_seqs = fasta_reader.read(target_file)
    if not target_seqs:
        print("Yarr! Error reading target fasta. Walk the plank.")
        sys.exit()

    gff_reader = GFFReader()
    print("Reading the scurvy " + gff_path + " file...")
    with open(gff_path, 'rb') as gff_file:
        cds_segment_lengths = gff_reader.read(gff_file)
    if not cds_segment_lengths:
        print("Yarr! Error reading GFF! Walk the plank.")
        sys.exit()

    boulder_io_reader = BoulderIOReader()
    print("Reading the scurvy " + excluded_primers_path + " file...")
    with open(excluded_primers_path, 'rb') as exclude_file:
        primers_to_exclude = boulder_io_reader.read_primer3_output(exclude_file)
    if not primers_to_exclude:
        print("Yarr! Error reading excluded primers file. Walk the plank.")

    primer3_options = ""
    print("Reading the scurvy " + options_path + " file...")
    with open(options_path, 'rb') as options_file:
        for line in options_file:
            primer3_options += line

    print("got " + str(len(target_seqs)) + " target seqs.")
    print("got " + str(len(cds_segment_lengths)) + " mrnas")

    # Prepare input for primer3_core
    print("Yarr! Preparing input for primer3_core...")
    boulder_formatter = BoulderIOFormatter()
    boulder_formatter.segment_lengths = cds_segment_lengths
    print("Yarr! Writing input file for primer3_core...")
    with open("target_seqs.boulder-io", "wb") as boulderfile:
        # write config data first
        boulderfile.write(primer3_options)
        exclude_entries = []
        for seq in target_seqs:
            for primer in primers_to_exclude:
                if primer.target_sequence.header == seq.header:
                    exclude_entries.append(primer.to_excluded_region_entry())
            boulderfile.write(boulder_formatter.format_seq(seq, exclude_entries))
            exclude_entries[:] = []
    
    # Run primer3_core
    print("Yarr! Running primer3_core!")
    os.system("primer3_core < target_seqs.boulder-io > primers.boulder-io")
    print("Yarr! Ran primer3_core!")
    
    # Verify 
    if file_is_empty("primers.boulder-io"):
        print("Yarr! No output from primer3_core! Walk the plank.")
        sys.exit()
    
    # Read primers from file
    print("Yarr! Reading output from primer3_core!")
    with open("primers.boulder-io", "rb") as primersfile:
        primers = boulder_io_reader.read_primer3_output(primersfile)

    # Verify again, just for fun
    if not primers:
        print("Yarr! No primers in the scurvy primers.boulder-io file! Walk the plank.")
        sys.exit()

    print("Yarr! We got " + str(len(primers)) + " scurvy primers!")

    # Convert primers.boulder-io file to left and right primer seqs, then write to fasta
    print("Yarr! Making scurvy fasta files of the left and right primers from the" +
            " primer3_core output. Shiver me timbers!")
    # TODO 
    with open("left_right_primers.fasta", "wb") as primersfasta:
        for primer in primers:
            primersfasta.write(primer.left_primer_to_fasta())
            primersfasta.write(primer.right_primer_to_fasta())
    
    # BLAST PRIMER SEQUENCES AGAINST GENOME TO MAKE SURE THEY ONLY AMPLIFY ONE REGION
        # blast left primers and right primers
        # filter hits for each using e-value and alignment length cutoffs
        # verify that for a given primer, the left and right each map to exactly one common region in the genome
        # TODO check that it's the right region????
        # discard primers where the left/right both mapped to 0 or >=2 regions
        # blastall -p blastn -d 454Scaffolds.fna -i primers_to_blast.fasta -r 1 -q 1 -G 1 -E 2 -W 9 -F "m D" -U -m 9 -b 4 > ../../BLAST_OUTPUT/primers_against_genome.blastout
        

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

def file_is_empty(path):
    return os.stat(path)[6] == 0

if __name__ == '__main__':
    main()

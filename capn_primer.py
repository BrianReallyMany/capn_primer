#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import subprocess
import os
import random
from src.dependency_checker import check_dependencies
from src.fasta_reader import FastaReader
from src.gff_reader import GFFReader
from src.boulder_io_formatter import BoulderIOFormatter
from src.boulder_io_reader import BoulderIOReader
from src.blast_output_parser import BlastOutputParser

## DEPENDENCIES: primer3_core, blastall, makeblastdb
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

    print("Shiver me timbers, the input files be present. Now I'll be reading them. Savvy?")

    # Read files
    print("Reading the scurvy " + target_fasta_path + " file...")
    fasta_reader = FastaReader()
    with open(target_fasta_path, 'rb') as target_file:
        target_seqs = fasta_reader.read(target_file)
    if not target_seqs:
        print("Yarr! Error reading target fasta. Walk the plank. " + random_insult() + "\n")
        sys.exit()

    gff_reader = GFFReader()
    print("Reading the scurvy " + gff_path + " file...")
    with open(gff_path, 'rb') as gff_file:
        cds_segment_lengths = gff_reader.read(gff_file)
    if not cds_segment_lengths:
        print("Yarr! Error reading GFF! Walk the plank. " + random_insult() + "\n")
        sys.exit()

    boulder_io_reader = BoulderIOReader()
    print("Reading the scurvy " + excluded_primers_path + " file...")
    with open(excluded_primers_path, 'rb') as exclude_file:
        primers_to_exclude = boulder_io_reader.read_primer3_output(exclude_file)
    if not primers_to_exclude:
        print("Yarr! Error reading excluded primers file. Walk the plank. " + random_insult() + "\n")

    primer3_options = ""
    print("Reading the scurvy " + options_path + " file...")
    with open(options_path, 'rb') as options_file:
        for line in options_file:
            primer3_options += line

    print("")

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
        print("Yarr! No output from primer3_core! Walk the plank. " + random_insult() + "\n")
        sys.exit()
    
    # Read primers from file
    print("Yarr! Reading output from primer3_core!")
    with open("primers.boulder-io", "rb") as primersfile:
        primers = boulder_io_reader.read_primer3_output(primersfile)

    # Verify again, just for fun
    if not primers:
        print("Yarr! No primers in the scurvy primers.boulder-io file! Walk the plank. " + random_insult() + "\n")
        sys.exit()

    print("Yarr! We got " + str(len(primers)) + " scurvy primers!")

    # Convert primers.boulder-io file to left and right primer seqs, then write to fasta
    print("Yarr! Making scurvy fasta files of the left and right primers from the" +
            " primer3_core output. Shiver me timbers!")
    with open("left_right_primers.fasta", "wb") as primersfasta:
        for primer in primers:
            primersfasta.write(primer.left_primer_to_fasta())
            primersfasta.write(primer.right_primer_to_fasta())

    # Verify that file was written
    if file_is_empty("left_right_primers.fasta"):
        print("Yarr! Left and right primers failed to write! Walk the plank. " + random_insult() + "\n")
        sys.exit()

    
    # BLAST PRIMER SEQUENCES AGAINST GENOME TO MAKE SURE THEY ONLY AMPLIFY ONE REGION
    print("Yarr! Preparing blast database!")
    # makeblastdb -in Bdor.Trinity.reallyfiltered.fasta -dbtype nucl
    os.system("makeblastdb -in genome.fasta -dbtype nucl > /dev/null")
    # Verify that the database was created
    if file_is_empty("genome.fasta.nhr"):
        print("Yarr! Database wasn't created. Walk the plank. " + random_insult() + "\n")
        sys.exit()

    print("Yarr! Running blast on those scurvy left and right primers...")
    os.system('blastall -p blastn -d genome.fasta -i left_right_primers.fasta '+
                '-r 1 -q 1 -G 1 -E 2 -W 9 -F "m D" -U -m 9 -b 4 > left_right_primers.blastout')
    
    # Verify that blast produced results
    if file_is_empty("left_right_primers.blastout"):
        print("Yarr! No output from blast! Walk the plank. " + random_insult() + "\n")
        sys.exit()

    print("Yarr! Blast finished running.")

    # Read in blast output
    blast_parser = BlastOutputParser()
    with open("left_right_primers.blastout", "rb") as blastout:
        blast_results = blast_parser.parse(blastout)

    if not blast_results or blast_results.number_of_hits == 0:
        print("Yarr! Scurvy error reading blast results. Walk the plank. " + random_insult() + "\n")
        sys.exit()
    
    print("Yarr! We got " + str(blast_results.number_of_hits()) + " hits!")
    print("Yarr! Time to filter these scurvy blast hits.")
    # filter hits for each using e-value and alignment length cutoffs
    MAX_E_VALUE = 0.5
    MIN_ALIGNMENT_LENGTH = 16
    blast_results.filter_results(MAX_E_VALUE, MIN_ALIGNMENT_LENGTH)
    print("Yarr! Now we got " + str(blast_results.number_of_hits()) + " hits!")

    # Verify that for a given primer, the left and right each map to exactly one common region in the genome
    one_match_primers = []
    for primer in primers:
        left_primer_name = primer.target_sequence.header
        left_primer_name += "_" + primer.primer_name + "_left"
        right_primer_name = primer.target_sequence.header
        right_primer_name += "_" + primer.primer_name + "_right"
        if blast_results.number_of_common_hits(left_primer_name, right_primer_name) == 1:
            one_match_primers.append(primer)
    print("Yarr! There be " + str(len(one_match_primers)) + " one-match primers. Yarr!")
    # TODO check that it's the right region????

    # Write those primers to a file or two
    with open("verified_primers.fasta", "wb") as primfasta:
        for primer in one_match_primers:
            #TODO
            pass

        

def verify_path(path):
    if not os.path.isfile(path):
        sys.stderr.write("Failed to find " + path + ". Walk the plank. " + random_insult() + "\n")
        sys.exit()

def file_is_empty(path):
    return os.stat(path)[6] == 0

def random_insult():
    insults = ["Ye scurvy dog.", "You son of a biscuit eater.", "Doubloons!",
            "You must be three sheets to the wind.", "Pegleg!"]
    return insults[random.randint(0, len(insults)-1)]

#####################################################################################

if __name__ == '__main__':
    main()

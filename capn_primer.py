#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

## DEPENDENCIES: primer3_core, exonerate, blast (?)
## data: any number of .fasta files representing in-species sequences (genome, transcriptome, etc.)
##       out-species genes of interest in nucleotide and protein fasta format
##       blast results a-plenty
##       alignment results from exonerate
##       various config data

## maybe work backwards -- given fasta file of sequences to create primers for, run primer3_core and then blast against reference to verify.
## then can add in previous exploration steps.

def main():
    print("Yarr! I be Cap'n Primer.")
    # CROSS-SPECIES CDS SEQUENCE EXPLORATION -- "in-species" (e.g. Bdor) and "out-species" (e.g. Dmel)
    # blast CDS of genes of interest from out-species against in-species genome
        # get cds.fasta for out-species
        # tweak headers of fasta somehow, magically
        # prepare blast database(s) for each in-species genome or whatever you wanna use
        # run blast against your in-species fastas using cross-species sequence exploration parameters

    # CROSS-SPECIES PROTEIN SEQUENCE EXPLORATION
    # blast translations (proteins) of genes of interest from out-species against in-species genome
        # get translations.fasta for out-species
        # tweak headers
        # run blast again, using protein-to-genome parameters

    # OK, ALL THAT GOT YOU WAS A BUNCH OF BLAST RESULTS. SO.

    # PARSING BLAST RESULTS
    # should have max e-value and min alignment length for blast hits
    # apparently 'filter_blast_hits.py' does this bit
    # so filter each set of blast results

    # should have priorities for each of the above in-species fastas
    # so somehow go through all the results in order of priority and, for each gene of interest, pick the first match.

    # GETTING SEQUENCES FOR MATCHING TRANSCRIPTS/CDSs
    # look into 'fasta_from_blast_hits.py' -- basically given original fasta and blast hit (contains indices?) write fasta of matching seq
    # do this for all the results (coming from multiple in-species fastas, remember)

    # TRIMMING SCAFFOLDS FOR GENOME ALIGNMENTS (?)
    # so apparently the step above gave us the whole dern scaffolds. which is fine for the transcriptome, but too much for the genome. so.
    # use exonerate to map the out-species genes of interest to their corresponding scaffolds
        # get a list of the out-species genes that mapped to the genome
        # get a fasta of those PROTEIN sequences
        # run exonerate --model protein2genome ...etc.
        # TODO maybe skip blast and just align? this was in my notes from before. because one gene actually aligned better to a different spot
    # exonerate outputs subsequences in fasta format
    # if any sequence is too short, use its indices (?) to pull a longer subsequence from original in-species fasta (?)

    # COMBINE ALL SEQUENCES INTO ONE FILE
    # the matches from all in-species fastas get turned into one big fasta.

    # ADD IN ANY OTHER KNOWN-INTERESTING IN-SPECIES TRANSCRIPTS TO FASTA

    # PREPARE INPUT FOR PRIMER3_CORE
        # make .boulder-io file
        # make primer_settings.conf file
        # cat 'em together

    # RUN PRIMER3_CORE

    # BLAST PRIMER SEQUENCES AGAINST GENOME TO MAKE SURE THEY ONLY AMPLIFY ONE REGION
        # concatenate left primer with reverse complement of right primer
        # make fasta
        # blastall against in-species genome (i guess) 
        # using e-value and alignment length cutoffs, discard matches you don't believe
        # each primer should have only one legit match. if it's got more than one, it's trasssh

        


if __name__ == '__main__':
    main()

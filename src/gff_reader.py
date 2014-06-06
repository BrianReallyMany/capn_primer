#!/usr/bin/env python

import sys
import copy

def parse_gff_attributes(attr):
    attr = attr.strip(' \t\n;').split(';') # Sanitize and split
    key_vals = [a.split('=') for a in attr]
    return dict(zip([kv[0] for kv in key_vals], [kv[1] for kv in key_vals]))

class GFFReader:

    def __init__(self):
        self.cds_segment_lengths = {}

    def read(self, io_buffer):
        cdss = []
        
        # Step 1: iterate through gff, make dictionary entries for mRNAs, store CDS for later
        for line in io_buffer:        
            if line.startswith("#"):
                continue
            columns = line.split('\t')
            if len(columns) != 9:
                # GFF used for testing contains an entire fasta inside,
                # line breaks in seqs and all. So printing to stderr or
                # raising exceptions is not an option here; we just try to recover
                continue
            attr = parse_gff_attributes(columns[8])
            if columns[2] == 'mRNA':
                self.cds_segment_lengths[attr['ID']] = []
            elif columns[2] == 'CDS':
                parents = attr["Parent"].split(",")
                for parent in parents:
                    attr2 = copy.deepcopy(attr)
                    attr2["Parent"] = parent
                    cdss.append([columns, attr2])
        
        # Step 2: Fill dictionary with CDS length values
        for cds in cdss:
            if not cds[1]['Parent'] in self.cds_segment_lengths:
                print("WARNING: Skipping CDS with no mRNA: "+cds[1]['ID'])
                continue
            
            self.cds_segment_lengths[cds[1]['Parent']].append(int(cds[0][4]) - int(cds[0][3]) + 1)

        return self.cds_segment_lengths
            

#!/usr/bin/env python

from src.blast_results_holder import BlastResultsHolder, BlastHit

class BlastOutputParser: 
    def __init__(self):
        self.results_holder = BlastResultsHolder()

    def parse(self, io_buffer):
        for line in io_buffer:
            fields = line.strip().split('\t')
            if line[0] == "#":
                continue
            elif len(fields) != 12:
                sys.stderr.write("BlastOutputParser ERROR: line length != 12 -- " + line + "\n")
                continue
            else:
                query_id = fields[0]
                subject_id = fields[1]
                percent_identity = float(fields[2])
                alignment_length = int(fields[3])
                subject_start = int(fields[8])
                subject_end = int(fields[9])
                e_value = float(fields[10])
                bit_score = float(fields[11])
                blast_hit = BlastHit(subject_id, percent_identity, alignment_length,
                                    subject_start, subject_end, e_value, bit_score)
                self.results_holder.add_result(query_id, blast_hit)
        return self.results_holder
                

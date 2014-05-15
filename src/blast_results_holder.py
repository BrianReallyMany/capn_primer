#!/usr/bin/env python

from collections import namedtuple

BlastHit = namedtuple("BlastHit", "subject_id percent_identity alignment_length subject_start subject_end e_value bit_score")

class BlastResultsHolder: 

    def __init__(self):
        self.results = {}

    def add_result(self, query_id, BlastHit):
        # TODO verify valid result ...
        if query_id in self.results:
            self.results[query_id].append(BlastHit)
        else:
            self.results[query_id] = [BlastHit]

    def number_of_hits(self):
        total = 0
        for query_id in self.results:
            total += len(self.results[query_id])
        return total

    def filter_results(self, max_e_value, min_alignment_length):
        for query_id in self.results:
            self.results[query_id] = [h for h in self.results[query_id] if
                    h.e_value < max_e_value and 
                    h.alignment_length > min_alignment_length]
            # 3-line list comprehension ?= ugly

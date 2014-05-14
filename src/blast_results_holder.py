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

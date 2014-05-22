#!/usr/bin/env python

import sys
from collections import namedtuple

BlastHit = namedtuple("BlastHit", "subject_id percent_identity alignment_length subject_start subject_end e_value bit_score")

class BlastResultsHolder: 

    # Any primers closer than this on the same seq will be considered a "match"
    MAX_PRODUCT_LENGTH = 400

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

    def number_of_common_hits(self, query1, query2):
        common_hits = 0
        if query1 not in self.results or query2 not in self.results:
            sys.stderr.write("BlastResultsHolder.number_of_common_hits KeyError -- ")
            sys.stderr.write("one of these query ids not valid: " + query1)
            sys.stderr.write(", " + query2 + "\n")
            return 0
        query1_hits = self.results[query1]
        query2_hits = self.results[query2]
        for q1_hit in query1_hits:
            for q2_hit in query2_hits:
                if self.close_enough(q1_hit, q2_hit):
                    common_hits += 1
        return common_hits

    def close_enough(self, hit1, hit2):
        if hit1.subject_id != hit2.subject_id:
            return False
        if abs(hit1.subject_start - hit2.subject_start) > self.MAX_PRODUCT_LENGTH:
            return False
        return True


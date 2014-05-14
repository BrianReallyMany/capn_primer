#!/usr/bin/env python

class BlastResultsHolder: 

    def __init__(self):
        self.results = {}

    def add_result(self, query_id, BlastHit):
        # TODO verify valid result ...
        if query_id in self.results:
            self.results[query_id].append(BlastHit)
        else:
            self.results[query_id] = [BlastHit]

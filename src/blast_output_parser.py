#!/usr/bin/env python

from src.blast_results_holder import BlastResultsHolder

class BlastOutputParser: 
    def __init__(self):
        self.results_holder = BlastResultsHolder()

    def parse(self, io_buffer):
        pass

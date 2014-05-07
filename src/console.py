#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from src.fasta_reader import FastaReader
from src.sequence import Sequence

class Controller:

    def __init__(self):
        self.seqs = []
        self.reader = FastaReader()


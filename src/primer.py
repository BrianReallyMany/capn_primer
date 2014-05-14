#!/usr/bin/env python

from src.sequence import Sequence
from src.translator import reverse_complement

class Primer:

    def __init__(self, primer_name=None, target_sequence=None, left_start=None,\
            left_length=None, right_start=None, right_length=None):
        if not primer_name:
            self.primer_name = ""
        self.primer_name = primer_name
        if not target_sequence:
            self.target_sequence = Sequence()
        self.target_sequence = target_sequence
        if not left_start:
            self.left_start = 0
        self.left_start = left_start
        if not left_length:
            self.left_length = 0
        self.left_length = left_length
        if not right_start:
            self.right_start = 0
        self.right_start = right_start
        if not right_length:
            self.right_length = 0
        self.right_length = right_length

    def left_primer_to_fasta(self):
        result = ">" + self.target_sequence.header + "_"
        result += self.primer_name + "_"
        result += "left\n"
        start = self.left_start + 1  # sequence.get_subseq is 1-based, not 0-based
        stop = start + self.left_length - 1
        result += self.target_sequence.get_subseq(start, stop)
        result += "\n"
        return result

    def right_primer_to_fasta(self):
        result = ">" + self.target_sequence.header + "_"
        result += self.primer_name + "_"
        result += "right\n"
        stop = self.right_start + 1  # confusingly enough; right primer is reversed
        start = stop - self.right_length + 1
        subseq = self.target_sequence.get_subseq(start, stop)
        result += reverse_complement(subseq)
        result += "\n"
        return result

    def product_to_fasta(self):
        result = ">" + self.target_sequence.header + "_"
        result += self.primer_name + "_"
        result += "product\n"
        start = self.left_start + 1
        stop = self.right_start + 1
        result += self.target_sequence.get_subseq(start, stop)
        result += "\n"
        return result

    def to_excluded_region_entry(self):
        result = "SEQUENCE_EXCLUDED_REGION="
        result += str(self.left_start) + ","
        length = self.right_start - self.left_start + 1
        result += str(length) + "\n"
        return result



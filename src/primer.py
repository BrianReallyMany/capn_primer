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

    def to_fasta(self):
        result = ">" + self.target_sequence.header + "_"
        result += self.primer_name + "\n"
        result += self.get_left_primer_sequence()
        result += self.get_right_primer_sequence()
        result += "\n"
        return result

    def left_primer_to_fasta(self):
        result = ">" + self.target_sequence.header + "_"
        result += self.primer_name + "_"
        result += "left\n"
        result += self.get_left_primer_sequence()
        result += "\n"
        return result

    def right_primer_to_fasta(self):
        result = ">" + self.target_sequence.header + "_"
        result += self.primer_name + "_"
        result += "right\n"
        result += self.get_right_primer_sequence()
        result += "\n"
        return result

    def product_to_fasta(self):
        result = ">" + self.target_sequence.header + "_"
        result += self.primer_name + "_"
        result += "product\n"
        result += self.get_product_sequence()
        result += "\n"
        return result

    def to_excluded_region_entry(self):
        result = "SEQUENCE_EXCLUDED_REGION="
        result += str(self.left_start) + ","
        length = self.right_start - self.left_start + 1
        result += str(length) + "\n"
        return result

    def to_table(self):
        result = self.primer_name + "\t"
        result += self.target_sequence.header + "\t"
        result += self.get_left_primer_sequence() + "\t"
        result += self.get_right_primer_sequence() + "\t"
        result += self.get_product_sequence() + "\n"
        return result

    def get_left_primer_sequence(self):
        start = self.left_start + 1  # sequence.get_subseq is 1-based, not 0-based
        stop = start + self.left_length - 1
        seq = self.target_sequence.get_subseq(start, stop)
        return seq
        
    def get_right_primer_sequence(self):
        stop = self.right_start + 1  # confusingly enough; right primer is reversed
        start = stop - self.right_length + 1
        subseq = self.target_sequence.get_subseq(start, stop)
        return reverse_complement(subseq)

    def get_product_sequence(self):
        start = self.left_start + 1
        stop = self.right_start + 1
        result = self.target_sequence.get_subseq(start, stop)
        return result

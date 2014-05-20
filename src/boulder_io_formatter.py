#!/usr/bin/env python

import sys

class BoulderIOFormatter:

    def __init__(self, primer_options=None):
        self.segment_lengths = {}
        if not primer_options:
            primer_options = {}
        self.primer3_core_options = primer_options

    def format_seq(self, seq, excluded_region_entries=None):
        """Writes Sequence object to boulder-io format.

        If optional excluded_region_entry argument is passed,
        appends these entries to the output.
        """
        result = "SEQUENCE_ID=" + seq.header + "\n"
        result += "SEQUENCE_TEMPLATE=" + seq.bases + "\n"
        if self.segment_lengths:
            lengths = self.segment_lengths[seq.header]
            total_length = 0
            for length in lengths[:-1]:
                total_length += length
                result += "SEQUENCE_TARGET=" + str(total_length) + ",1\n"
        if excluded_region_entries:
            for entry in excluded_region_entries:
                result += entry
        result += "=\n"
        return result
        


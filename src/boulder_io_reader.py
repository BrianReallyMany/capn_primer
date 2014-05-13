#!/usr/bin/env python

import re
from src.sequence import Sequence
from src.primer import Primer

class BoulderIOReader: 
    def __init__(self, primer_options=None):
        self.current_seq = None

    def entry_to_primers(self, entry):
        target_sequence = Sequence()
        current_primer = Primer()
        primers = []
        for line in entry.split('\n'):
            splitline = line.strip().split('=')
            if len(splitline) != 2:
                # end of entry or something wrong...
                # try to fail gracefully
                return primers
            if splitline[0] == "SEQUENCE_ID":
                target_sequence.header = splitline[1]
            elif "SEQUENCE_TEMPLATE" in splitline[0]:
                target_sequence.bases = splitline[1]
            elif "PRIMER_LEFT" in splitline[0]:
                # match "PRIMER_LEFT_0" but not e.g. "PRIMER_LEFT_0_SEQUENCE"
                m = re.search('[0-9]+$', splitline[0])
                if m:
                    number = m.group(0)
                    current_primer.primer_name = "primer_" + str(number)
                    current_primer.target_sequence = target_sequence
                    start_and_length = splitline[1].split(',')
                    start = start_and_length[0]
                    length = start_and_length[1]
                    current_primer.left_start = start
                    current_primer.left_length = length
            elif "PRIMER_RIGHT" in splitline[0]:
                # match "PRIMER_LEFT_0" but not e.g. "PRIMER_LEFT_0_SEQUENCE"
                m = re.search('[0-9]+$', splitline[0])
                if m:
                    start_and_length = splitline[1].split(',')
                    start = start_and_length[0]
                    length = start_and_length[1]
                    current_primer.right_start = start
                    current_primer.right_length = length
                    # At this point we should have a complete primer
                    if current_primer.primer_name and current_primer.target_sequence.bases:
                        primers.append(current_primer)
                        current_primer = Primer()
                    else:
                        sys.stderr.write("BoulderIOReader ERROR: reached end of primer info ")
                        sys.stderr.write("but primer is incomplete:\nat this line:\n" + line + "\n")
                        sys.stderr.write("Will discard this primer and attempt to continue.\n")
                        current_primer = Primer()
        return primers

    def read_primer3_output(self, io_buffer):
        primers = []
        current_entry = ""
        for line in io_buffer:
            if line.strip() == "=":
                # end of an entry
                primers.extend(self.entry_to_primers(current_entry))
                current_entry = ""
            else:
                current_entry += line
        return primers



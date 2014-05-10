#!/usr/bin/env python

import re
from src.translator import reverse_complement
from src.sequence import Sequence

class BoulderIOReader:

    def __init__(self, primer_options=None):
        self.current_seq = None

    def entry_to_primer_seqs(self, entry):
        seqs = []
        current_header = ""
        current_primer = ""
        for line in entry.split('\n'):
            splitline = line.strip().split('=')
            if not splitline[0]:
                # end of entry
                return seqs
            if splitline[0] == "SEQUENCE_ID":
                current_header = splitline[1]
                continue
            elif "PRIMER_LEFT" in splitline[0] and "SEQUENCE" in splitline[0]:
                # left primer sequence
                # get sequence number:
                m = re.search('[0-9]+', splitline[0])
                if not m.group():
                    continue
                number = m.group(0)
                # add primer sequence to current_primer
                current_primer += splitline[1]
                continue
            elif "PRIMER_RIGHT" in splitline[0] and "SEQUENCE" in splitline[0]:
                # right primer sequence
                # get sequence number
                m = re.search('[0-9]+', splitline[0])
                if not m.group():
                    continue
                number = m.group(0)
                current_primer += reverse_complement(splitline[1])
                primer_header = current_header + "_primer_" + number
                seqs.append(Sequence(primer_header, current_primer))            
        return seqs

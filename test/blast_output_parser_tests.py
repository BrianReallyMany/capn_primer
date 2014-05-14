#!/usr/bin/env python

import unittest
import io
from src.blast_output_parser import BlastOutputParser
from src.blast_results_holder import BlastResultsHolder

class TestBlastOutputParser(unittest.TestCase):

    def setUp(self):
        self.parser = BlastOutputParser()
        self.input_data = io.BytesIO("""\
# BLASTN 2.2.25 [Feb-01-2011]
# Query: comp24970_c0_seq1_primer0
# Database: 454Scaffolds.fna
# Fields: Query id, Subject id, % identity, alignment length, mismatches, gap openings, q. start, q. end, s. start, s. end, e-value, bit score
comp24970_c0_seq1_primer0	scaffold00128	100.00	23	0	0	24	46	549870	549848	2e-04	46.1
comp24970_c0_seq1_primer0	scaffold00128	100.00	23	0	0	1	23	550156	550134	2e-04	46.1
comp24970_c0_seq1_primer0	scaffold00105	100.00	18	0	0	14	31	636373	636356	0.16	36.2
comp24970_c0_seq1_primer0	scaffold00181	100.00	17	0	0	13	29	18742	18758	0.61	34.2
comp24970_c0_seq1_primer0	scaffold00134	100.00	17	0	0	16	32	410149	410165	0.61	34.2
""")

    def test_parse(self):
        results_holder = self.parser.parse(self.input_data)
        self.assertTrue(results_holder)
        blast_hits_for_comp24970_etc = results_holder.results["comp24970_c0_seq1_primer0"]
        third_blast_hit = blast_hits_for_comp24970_etc[2]
        self.assertEquals(36.2, third_blast_hit.bit_score)


    


##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBlastOutputParser))
    return suite

if __name__ == '__main__':
    unittest.main()

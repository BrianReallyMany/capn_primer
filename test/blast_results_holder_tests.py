#!/usr/bin/env python

import unittest
from collections import namedtuple
from src.blast_results_holder import BlastResultsHolder

BlastHit = namedtuple("BlastHit", "subject_id percent_identity alignment_length subject_start subject_end e_value bit_score")
# Fields: Query id, Subject id, % identity, alignment length, mismatches, gap openings, q. start, q. end, s. start, s. end, e-value, bit score

class TestBlastResultsHolder(unittest.TestCase):

    def setUp(self):
        self.holder = BlastResultsHolder()

    def test_add_result(self):
        self.assertEquals(0, len(self.holder.results))
        query_id = "foo_primer"
        result = BlastHit("foo_seq", 100.00, 23, 100, 122, 2e-04, 46.1)
        self.holder.add_result(query_id, result)
        self.assertEquals(1, len(self.holder.results))

    def test_add_two_results(self):
        self.assertEquals(0, len(self.holder.results))
        query_id = "foo_primer"
        result = BlastHit("foo_seq", 100.00, 23, 100, 122, 2e-04, 46.1)
        self.holder.add_result(query_id, result)
        self.holder.add_result(query_id, result)
        self.assertEquals(1, len(self.holder.results))
        self.assertEquals(2, len(self.holder.results[query_id]))

##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBlastResultsHolder))
    return suite

if __name__ == '__main__':
    unittest.main()
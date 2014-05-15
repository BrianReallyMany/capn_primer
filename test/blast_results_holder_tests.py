#!/usr/bin/env python

import unittest
from src.blast_results_holder import BlastResultsHolder, BlastHit

class TestBlastResultsHolder(unittest.TestCase):

    def setUp(self):
        self.holder = BlastResultsHolder()

    def add_a_result(self):
        query_id = "foo_primer"
        result = BlastHit("foo_seq", 100.00, 23, 100, 122, 2e-04, 46.1)
        self.holder.add_result(query_id, result)

    def test_add_result(self):
        self.assertEquals(0, len(self.holder.results))
        self.add_a_result()
        self.assertEquals(1, len(self.holder.results))

    def test_add_two_results(self):
        self.assertEquals(0, len(self.holder.results))
        self.add_a_result()
        self.add_a_result()
        self.assertEquals(1, len(self.holder.results))
        #self.assertEquals(2, len(self.holder.results[query_id]))

    def test_number_of_hits(self):
        self.add_a_result()
        self.add_a_result()
        query_id2 = "bar_primer"
        result2 = BlastHit("foo_seq", 100.00, 23, 100, 122, 2e-04, 46.1)
        self.holder.add_result(query_id2, result2)
        # added 3 total blast hits
        self.assertEquals(3, self.holder.number_of_hits())

    def test_filter_results(self):
        query_id = "foo_primer"
        result1 = BlastHit("foo_seq", 100.00, 23, 100, 122, 2e-04, 46.1)
        result2 = BlastHit("foo_seq", 100.00, 15, 100, 122, 2e-04, 46.1)
        result3 = BlastHit("foo_seq", 100.00, 23, 100, 122, 0.7, 46.1)
        for result in [result1, result2, result3]:
            self.holder.add_result(query_id, result)
        self.assertEquals(3, len(self.holder.results[query_id]))
        self.holder.filter_results(0.5, 16)
        self.assertEquals(1, len(self.holder.results[query_id]))

    ### These next tests get a little ugly. We are going to add blast hits with
    ### different query ids that are close together (just like left/right primers...)
    ### We should be told that they produced one common hit. We'll then add extra hits
    ### for the query ids that are far apart, and the answer shouldn't change.
    ### However, when we add hits for the query ids that are also close (but located elsewhere)
    ### we should be told that there are 2 common hits. Here goes.
    def setup_results_with_no_common_hits(self):
        left = "primer_left"
        right = "primer_right"
        result1 = BlastHit("foo_seq", 100, 23, 100, 122, 2e-04, 40)
        self.holder.add_result(left, result1)
        result2 = BlastHit("bar_seq", 100, 23, 170, 192, 2e-04, 40)
        self.holder.add_result(right, result2)
        # They're close together indices-wise, but on different seqs. No match!

        result3 = BlastHit("foo_seq", 100, 23, 4000, 4022, 2e-04, 40)
        self.holder.add_result(right, result3)
        # Here's a right primer hit on the same seq as the left primer hit, but it's thousands of
        #  bases away. No match!

    def test_number_of_common_hits(self):
        self.setup_results_with_no_common_hits()
        self.assertEquals(0, self.holder.number_of_common_hits("primer_left", "primer_right"))


##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBlastResultsHolder))
    return suite

if __name__ == '__main__':
    unittest.main()

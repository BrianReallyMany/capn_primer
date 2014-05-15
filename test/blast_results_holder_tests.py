#!/usr/bin/env python

import unittest
from src.blast_results_holder import BlastResultsHolder, BlastHit

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

    def test_number_of_hits(self):
        query_id1 = "foo_primer"
        result1 = BlastHit("foo_seq", 100.00, 23, 100, 122, 2e-04, 46.1)
        self.holder.add_result(query_id1, result1)
        self.holder.add_result(query_id1, result1)
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

##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBlastResultsHolder))
    return suite

if __name__ == '__main__':
    unittest.main()

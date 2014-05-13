#!/usr/bin/env python

import unittest
from src.boulder_io_formatter import BoulderIOFormatter
from src.sequence import Sequence

class TestBoulderIOFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = BoulderIOFormatter()
        self.formatter.segment_lengths = {"foo_mrna": [5, 7]}
        self.seq1 = Sequence("foo_mrna", "GATTACAGATTACA")

    def test_format_seq(self):
        expected = "SEQUENCE_ID=foo_mrna\n"
        expected += "SEQUENCE_TEMPLATE=GATTACAGATTACA\n"
        expected += "SEQUENCE_TARGET=5,1\n=\n"
        actual = self.formatter.format_seq(self.seq1)
        self.assertEquals(actual, expected)

    def test_format_seq_with_excluded_region_entries(self):
        excluded_entries = ["SEQUENCE_EXCLUDED_REGION=2,11\n"]
        expected = "SEQUENCE_ID=foo_mrna\n"
        expected += "SEQUENCE_TEMPLATE=GATTACAGATTACA\n"
        expected += "SEQUENCE_TARGET=5,1\n"
        expected += "SEQUENCE_EXCLUDED_REGION=2,11\n=\n"
        actual = self.formatter.format_seq(self.seq1, excluded_entries)
        self.assertEquals(actual, expected)


    

##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBoulderIOFormatter))
    return suite

if __name__ == '__main__':
    unittest.main()

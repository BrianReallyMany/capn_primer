#!/usr/bin/env python

import unittest
from mock import Mock
from src.primer import Primer
from src.sequence import Sequence

class TestPrimer(unittest.TestCase):

    def setUp(self):
        self.seq1 = Sequence("foo_seq", "GATTACAGATTACA")
        self.primer1 = Primer("primer1", self.seq1, 2, 3, 12, 4)
        # Just for reference, that means left primer = "TTA",
        # right primer is reverse complement of "TTAC" => "GTAA"

    def test_left_primer_to_fasta(self):
        expected = ">foo_seq_primer1_left\nTTA\n"
        self.assertEquals(self.primer1.left_primer_to_fasta(), expected)

    def test_right_primer_to_fasta(self):
        expected = ">foo_seq_primer1_right\nGTAA\n"
        self.assertEquals(self.primer1.right_primer_to_fasta(), expected)

    def test_product_to_fasta(self):
        expected = ">foo_seq_primer1_product\nTTACAGATTAC\n"
        self.assertEquals(self.primer1.product_to_fasta(), expected)

    def test_to_excluded_region_entry(self):
        expected = "SEQUENCE_EXCLUDED_REGION=2,11\n"
        self.assertEquals(self.primer1.to_excluded_region_entry(), expected)

    def test_to_fasta(self):
        expected = ">foo_seq_primer1\n"
        expected += "TTAGTAA\n"
        self.assertEquals(self.primer1.to_fasta(), expected)


##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPrimer))
    return suite

if __name__ == '__main__':
    unittest.main()

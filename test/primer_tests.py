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
        expected = "foo_seq_primer1_left\nTTA\n"
        self.assertEquals(self.primer1.left_primer_to_fasta(), expected)


##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPrimer))
    return suite

if __name__ == '__main__':
    unittest.main()

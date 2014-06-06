#!/usr/bin/env python

import unittest
import io
from src.gff_reader import *

class TestGFFReader(unittest.TestCase):

    def setUp(self):
        self.reader = GFFReader()
    
    def test_parse_gff_attributes(self):
        attr = "\t; foo=dog;baz=bub;  \t\n"
        self.assertEquals(parse_gff_attributes(attr), {"foo":"dog", "baz":"bub"})

    def test_read(self):
        gff = io.BytesIO('seq\tGeibBase\tCDS\t1\t42\t.\t+\t0\tID=foo-RA:CDS1;Parent=foo-RA\n'+\
        'seq\tGeibBase\tmRNA\t1\t200\t.\t+\t0\tID=foo-RA\n'+\
        'seq\tGeibBase\tmRNA\t1\t200\t.\t+\t0\tID=foo-RB\n'+\
        'seq\tGeibBase\tCDS\t50\t100\t.\t+\t0\tID=foo-RA:CDS2;Parent=foo-RA,foo-RB\n'+\
        'seq\tGeibBase\tCDS\t120\t180\t.\t+\t0\tID=foo-RA:CDS3;Parent=foo-RA\n')

        segment_lengths = self.reader.read(gff)

        expected = {'foo-RA':[42, 51, 61], 'foo-RB':[51]}
        self.assertEqual(segment_lengths, expected)


##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGFFReader))
    return suite

if __name__ == '__main__':
    unittest.main()

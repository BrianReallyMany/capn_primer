#!/usr/bin/env python

# import all the lovely files
import unittest
import test.fasta_reader_tests
import test.gff_reader_tests
import test.sequence_tests
import test.dependency_checker_tests
import test.boulder_io_formatter_tests

# get suites from test modules
suites = [
test.fasta_reader_tests.suite(),\
test.gff_reader_tests.suite(),\
test.sequence_tests.suite(),\
test.dependency_checker_tests.suite(),\
test.boulder_io_formatter_tests.suite()\
]

# collect suites in a TestSuite object
suite = unittest.TestSuite()
for s in suites:
    suite.addTest(s)

# run suite
unittest.TextTestRunner(verbosity=2).run(suite)

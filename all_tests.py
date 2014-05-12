#!/usr/bin/env python

# import all the lovely files
import unittest
import test.fasta_reader_tests
import test.gff_reader_tests
import test.sequence_tests
import test.dependency_checker_tests
import test.boulder_io_formatter_tests
import test.translator_tests
import test.boulder_io_reader_tests
import test.primer_tests

# get suites from test modules
suites = [
test.fasta_reader_tests.suite(),\
test.gff_reader_tests.suite(),\
test.sequence_tests.suite(),\
test.dependency_checker_tests.suite(),\
test.boulder_io_formatter_tests.suite(),\
test.translator_tests.suite(),\
test.boulder_io_reader_tests.suite(),\
test.primer_tests.suite()\
]

# collect suites in a TestSuite object
suite = unittest.TestSuite()
for s in suites:
    suite.addTest(s)

# run suite
unittest.TextTestRunner(verbosity=2).run(suite)

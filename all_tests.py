#!/usr/bin/env python

# import all the lovely files
import unittest
import test.fasta_reader_tests
import test.sequence_tests
import test.console_tests
import test.dependency_checker_tests

# get suites from test modules
suite1 = test.fasta_reader_tests.suite()
suite2 = test.sequence_tests.suite()
suite3 = test.console_tests.suite()
suite4 = test.dependency_checker_tests.suite()

# collect suites in a TestSuite object
suite = unittest.TestSuite()
suite.addTest(suite1)
suite.addTest(suite2)
suite.addTest(suite3)
suite.addTest(suite4)

# run suite
unittest.TextTestRunner(verbosity=2).run(suite)

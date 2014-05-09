#!/usr/bin/env python

import unittest
from src.dependency_checker import command_is_available

class TestDependencyChecker(unittest.TestCase):

    def test_command_is_available(self):
        self.assertFalse(command_is_available("bar"))
        self.assertTrue(command_is_available("echo"))


##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDependencyChecker))
    return suite

if __name__ == '__main__':
    unittest.main()

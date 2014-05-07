#!/usr/bin/env python

import unittest
from src.console import Controller

class TestController(unittest.TestCase):

    def setUp(self):
        self.ctrlr = Controller()


##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestController))
    return suite

if __name__ == '__main__':
    unittest.main()

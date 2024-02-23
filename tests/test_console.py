#!/usr/bin/python3
"""
Unit Test Class
"""
import unittest
from datetime import datetime
import json
import console

HBNBCommand = console.HBNBCommand


class TestHBNBCommandDocs(unittest.TestCase):
    """BaseModel """

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('.......  For the Console  .......')
        print('.................................\n\n')

    def test_doc_file(self):
        """ the file"""
        expected = '\nCommand interpreter for Holberton AirBnB project\n'
        actual = console.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """ the class"""
        expected = '\n        Command inerpreter class\n    '
        actual = HBNBCommand.__doc__
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main

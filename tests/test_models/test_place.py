#!/usr/bin/python3
"""
Unit Test for Place Class
"""
import unittest
from datetime import datetime
import json
import models
import os

Place = models.place.Place
BaseModel = models.base_model.BaseModel
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class TestPlaceDocs(unittest.TestCase):
    """testing BaseModel """

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('........   Place Class   ........')
        print('.................................\n\n')

    def test_doc_file(self):
        """the file"""
        expected = '\nPlace Class from Models Module\n'
        actual = models.place.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """the class"""
        expected = 'Place class handles all application places'
        actual = Place.__doc__
        self.assertEqual(expected, actual)


class TestPlaceInstances(unittest.TestCase):
    """testing for  instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('....... Testing Functions .......')
        print('.........  Place Class  .........')
        print('.................................\n\n')

    def setUp(self):
        """start new place for testing"""
        self.place = Place()

    def test_instantiation(self):
        """Place instantiated"""
        self.assertIsInstance(self.place, Place)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_to_string(self):
        """BaseModel casted to string"""
        my_str = str(self.place)
        my_list = ['Place', 'id', 'created_at']
        actual = 0
        for sub_str in my_list:
            if sub_str in my_str:
                actual += 1
        self.assertTrue(3 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_instantiation_no_updated(self):
        """not have updated attribute"""
        my_str = str(self.place)
        actual = 0
        if 'updated_at' in my_str:
            actual += 1
        self.assertTrue(0 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_updated_at(self):
        """function should add updated_at attribute"""
        self.place.save()
        actual = type(self.place.updated_at)
        expected = type(datetime.now())
        self.assertEqual(expected, actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_to_json(self):
        """should return serializable dict object"""
        self.place_json = self.place.to_json()
        actual = 1
        try:
            serialized = json.dumps(self.place_json)
        except:
            actual = 0
        self.assertTrue(1 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_json_class(self):
        """  include class key with value Place"""
        self.place_json = self.place.to_json()
        actual = None
        if self.place_json['__class__']:
            actual = self.place_json['__class__']
        expected = 'Place'
        self.assertEqual(expected, actual)

    def test_guest_attribute(self):
        """ guest attribute"""
        self.place.max_guest = 3
        if hasattr(self.place, 'max_guest'):
            actual = self.place.max_guest
        else:
            actual = ''
        expected = 3
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main

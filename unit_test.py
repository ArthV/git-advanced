import unittest
import os
import sys

from  main import format_data


class SimlpeUnitTest(unittest.TestCase):

    def test_is_ok(self):
        input_dict: dict = {}
        input_dict['title'] = {'value': 'test'}
        input_dict['details'] = {'description': {'value': 'test'}, 'urls': {'webLaunch': 'test'},
         'classifications': [{'associatedClassification': {'name': {'value': 'test'}}}]}
        input_dict['urn'] = "test"

        output_value = format_data(input_dict)

        self.assertEqual(output_value, ['test', 'test', 'test', 'test', 'test'])

import unittest
import requests
import json
from pyramid import testing


class ViewTests(unittest.TestCase):

    def setUp(self):
        self.rest_url = 'http://api.brlight.net/api'

    def test_get_orgao(self):
        """
        Get órgãos cadastrados!
        """
        url = self.rest_url + '/orgao_sg/doc'
        get = requests.get(url)

        assert(url)

    def tearDown(self):
        testing.tearDown()


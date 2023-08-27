# tests/test_api.py
import unittest
from unittest.mock import patch
import json
import sys

# Monkeypatch our local copy of the bird module
sys.path.append('.')

from bird.core.api import OAIApi, OAIApiException

class TestOAIApi(unittest.TestCase):

    @patch('requests.post')
    def test_make_request_successful(self, mock_post):
        # Mock a successful API response
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            'choices': [
                {'text': 'Test response'}
            ]
        })

        api = OAIApi(api_key='test_api_key', endpoint='http://test.endpoint', max_tokens=100)
        result = api.make_request('Test prompt')

        self.assertEqual(result, 'Test response')

    @patch('requests.post')
    def test_make_request_unsuccessful(self, mock_post):
        # Mock an unsuccessful API response
        mock_response = mock_post.return_value
        mock_response.status_code = 400
        mock_response.text = 'Bad Request'

        api = OAIApi(api_key='test_api_key', endpoint='http://test.endpoint', max_tokens=100)

        with self.assertRaises(OAIApiException):
            api.make_request('Test prompt')

    def test_from_config(self):
        api = OAIApi.from_config(endpoint='http://test.endpoint', api_key='test_api_key', max_tokens=100)

        self.assertIsInstance(api, OAIApi)
        self.assertEqual(api.api_key, 'test_api_key')
        self.assertEqual(api.endpoint, 'http://test.endpoint')
        self.assertEqual(api.max_tokens, 100)

if __name__ == '__main__':
    unittest.main()

# tests/test_util.py
import unittest
from unittest.mock import patch, mock_open
import json
import sys

# Monkeypatch our local copy of the bird module
sys.path.append('.')

from bird.core.util import load_config, validate_config

class TestUtil(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "endpoint": "http://localhost:8081/",
        "api_key": "1234567890",
        "max_tokens": 100,
        "bird_data_path": "data/birds.json",
        "prompt_data_path": "data/prompts.json"
    }))
    def test_load_config(self, mock_file):
        config = load_config('fake_path')
        self.assertEqual(config['endpoint'], "http://localhost:8081/")
        self.assertEqual(config['api_key'], "1234567890")
        self.assertEqual(config['max_tokens'], 100)
        self.assertEqual(config['bird_data_path'], "data/birds.json")
        self.assertEqual(config['prompt_data_path'], "data/prompts.json")

    def test_validate_config(self):
        valid_config = {
            "endpoint": "http://localhost:8081/",
            "api_key": "1234567890",
            "max_tokens": 100,
            "bird_data_path": "data/birds.json",
            "prompt_data_path": "data/prompts.json"
        }
        # This should not raise any exceptions
        validate_config(valid_config)

    def test_validate_config_missing_key(self):
        invalid_config = {
            "endpoint": "http://localhost:8081/",
            "api_key": "1234567890",
            "max_tokens": 100,
            "bird_data_path": "data/birds.json"
            # "prompt_data_path" is missing
        }
        with self.assertRaises(ValueError):
            validate_config(invalid_config)

    def test_validate_config_invalid_max_tokens(self):
        invalid_config = {
            "endpoint": "http://localhost:8081/",
            "api_key": "1234567890",
            "max_tokens": "100",  # Should be an int, not a string
            "bird_data_path": "data/birds.json",
            "prompt_data_path": "data/prompts.json"
        }
        with self.assertRaises(ValueError):
            validate_config(invalid_config)

if __name__ == '__main__':
    unittest.main()

# tests/test_prompter.py
import unittest
from unittest.mock import patch, mock_open
import json
import sys

# Monkeypatch our local copy of the bird module
sys.path.append('.')

from bird.core.prompter import Prompter
from bird.model.prompt import Prompt

class TestPrompter(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "Compliment": {
            "description": "Compliments",
            "prompts": ["You look great"]
        },
        "Insult": {
            "description": "Insults",
            "prompts": ["You're terrible"]
        }
    }))
    def test_load_prompts(self, mock_file):
        prompts = Prompter.load_prompts('fake_path')
        self.assertIsInstance(prompts['Compliment'], Prompt)
        self.assertEqual(prompts['Compliment'].get_prompt(), "You look great")
        self.assertEqual(prompts['Insult'].get_prompt(), "You're terrible")

    @patch('bird.core.prompter.Prompter.load_prompts')
    def test_from_config(self, mock_load_prompts):
        mock_load_prompts.return_value = {'Compliment': Prompt('Compliment', 'desc', ['You look great'])}
        prompter = Prompter.from_config('fake_path')
        self.assertIsInstance(prompter, Prompter)
        
    def test_get_prompt(self):
        prompts = {
            'Compliment': Prompt('Compliment', 'desc', ['You look great']),
            'Insult': Prompt('Insult', 'desc', ['You\'re terrible'])
        }
        prompter = Prompter(prompts=prompts)
        self.assertEqual(prompter.get_prompt('Compliment'), "You look great")
        self.assertEqual(prompter.get_prompt('Insult'), "You\'re terrible")
        self.assertIsNone(prompter.get_prompt('Unknown'))

if __name__ == '__main__':
    unittest.main()

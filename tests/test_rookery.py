# tests/test_rookery.py
import unittest
from unittest.mock import patch, mock_open
import json
import sys

# Monkeypatch our local copy of the bird module
sys.path.append('.')

from bird.core.rookery import Rookery
from bird.model.bird import Bird

# Create a more complete mock Bird object
mock_bird = Bird(
    bird_id=1, 
    name='Reginald', 
    species='Red Cardinal', 
    persona='Shakespeare', 
    description='Some description', 
    promptMeta=['Meta info'], 
    physicalDetails='Details', 
    customStyle={}
)

class TestRookery(unittest.TestCase):

    def test_init(self):
        birds = {'Reginald': mock_bird}
        rookery = Rookery(birds=birds)
        self.assertEqual(rookery.birds, birds)

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([{
        'bird_id': 1,
        'name': 'Reginald',
        'species': 'Red Cardinal',
        'persona': 'Shakespeare',
        'description': 'Some description',
        'promptMeta': ['Meta info'],
        'physicalDetails': 'Details',
        'customStyle': {}
    }]))
    def test_load_birds(self, mock_file):
        birds = Rookery.load_birds('fake_path')
        self.assertIsInstance(birds['Reginald'], Bird)
        self.assertEqual(birds['Reginald'].name, 'Reginald')

    @patch('builtins.open', new_callable=mock_open, read_data='not json')
    def test_load_birds_invalid_data(self, mock_file):
        with self.assertRaises(ValueError):
            Rookery.load_birds('fake_path')

    @patch('bird.core.rookery.Rookery.load_birds')  # Mock the static method load_birds
    def test_from_config(self, mock_load_birds):
        mock_load_birds.return_value = {'Reginald': mock_bird}
        rookery = Rookery.from_config('fake_path')
        self.assertIsInstance(rookery, Rookery)
        self.assertEqual(rookery.birds['Reginald'].name, 'Reginald')

    def test_get_bird(self):
        birds = {'Reginald': mock_bird}
        rookery = Rookery(birds=birds)
        bird = rookery.get_bird('Reginald')
        self.assertEqual(bird.name, 'Reginald')

    def test_get_bird_not_found(self):
        birds = {'Reginald': mock_bird}
        rookery = Rookery(birds=birds)
        bird = rookery.get_bird('NotReginald')
        self.assertIsNone(bird)

if __name__ == '__main__':
    unittest.main()

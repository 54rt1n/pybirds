# tests/test_generator.py
import unittest
from unittest.mock import patch, Mock
import sys

# Monkeypatch our local copy of the bird module
sys.path.append('.')

from bird.core.generator import PhraseWizard
from bird.core.api import OAIApi
from bird.model.bird import Bird

class TestPhraseWizard(unittest.TestCase):
    
    def test_factory(self):
        api_mock = Mock(spec=OAIApi)
        wizard = PhraseWizard.factory(api=api_mock)
        self.assertIsInstance(wizard, PhraseWizard)
        
    @patch.object(OAIApi, 'make_request')
    def test_generate_phrase(self, mock_make_request):
        mock_make_request.return_value = "Generated text"

        api_mock = OAIApi(api_key="test_key", endpoint="test_endpoint", max_tokens=50)
        api_mock.make_request = mock_make_request

        wizard = PhraseWizard(api=api_mock)

        bird_mock = Mock(spec=Bird)
        bird_mock.name = "TestBird"
        bird_mock.persona = "TestPersona"
        bird_mock.description = "TestDescription"

        prompts = ["be witty"]
        bird_name = "TestBird"
        styles = ["Funny"]

        result = wizard.generate_phrase(bird=bird_mock, prompts=prompts, bird_name=bird_name, styles=styles)

        self.assertEqual(result, "Generated text")
        mock_make_request.assert_called_once()


if __name__ == '__main__':
    unittest.main()

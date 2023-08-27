# core/generator.py - Martin Bukowski - 2023-08-26
from typing import List, Dict, Any
import logging
from .api import OAIApi
from ..model.bird import Bird

logger = logging.getLogger(__name__)

class PhraseWizard:
    """Generates phrases based on bird personalities and styles."""
    
    def __init__(self, api: OAIApi):
        """Initialize the PhraseWizard with an API client.

        Args:
            api (OAIApi): The API client for generating text.
        """
        self.api = api

    @classmethod
    def factory(cls, api: OAIApi) -> 'PhraseWizard':
        """Factory method to create a new PhraseWizard instance.

        Args:
            api (OAIApi): The API client for generating text.

        Returns:
            PhraseWizard: A new PhraseWizard instance.
        """
        return cls(api=api)

    def generate_phrase(self, bird: Bird, prompts: List[str], styles: List[str], **kwargs: Any) -> str:
        """Generate a phrase based on the given bird, prompts, and styles.

        Args:
            bird (Bird): The bird character for which to generate a phrase.
            prompts (List[str]): The prompts to guide the phrase generation.
            styles (List[str]): The styles to apply to the phrase.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            str: The generated phrase.
            
        Raises:
            Exception: Rethrows any known exceptions encountered during phrase generation.
        """

        # TODO we need to make this a multi-shot prompt

        prompt = f"""Character: {bird.name}
Persona: {bird.persona}
Description: {bird.description}
Generate a phrase for this character.  It should be {', '.join(prompts)}.
{bird.name} [{','.join(styles)}]: \""""
        
        # Generate the phrase using the API
        try:
            generated_text = self.api.make_request(prompt=prompt)
            return generated_text
        except Exception as e:
            logger.error(f"Failed to generate phrase for bird {bird.name}: {e}")
            raise e
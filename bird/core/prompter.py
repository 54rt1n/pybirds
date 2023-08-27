# core/prompter.py - Martin Bukowski - 2023-08-26
import json
import logging
from typing import Dict, Optional
from ..model.prompt import Prompt

logger = logging.getLogger(__name__)

class Prompter:
    """Handles the management and retrieval of prompts based on different styles."""
    
    def __init__(self, prompts: Dict[str, Prompt]):
        """Initialize a new Prompter object.

        Args:
            prompts (Dict[str, Prompt]): Dictionary mapping style names to Prompt objects.
        """
        self.prompts = prompts

    @classmethod
    def from_config(cls, prompt_data_path: str, **config) -> 'Prompter':
        """Create a new Prompter object from a configuration file.

        Args:
            prompt_data_path (str): The path to the JSON file containing prompt data.
            **config: Additional configuration options (not currently used).

        Returns:
            Prompter: A new Prompter object.
        """
        prompts = cls.load_prompts(prompt_data_path)
        return cls(prompts=prompts)

    @staticmethod
    def load_prompts(prompt_data_path: str) -> Dict[str, Prompt]:
        """Load prompts from a JSON file.

        Args:
            prompt_data_path (str): The path to the JSON file containing prompt data.

        Returns:
            Dict[str, Prompt]: A dictionary mapping style names to Prompt objects.
        """
        try:
            with open(prompt_data_path, 'r') as f:
                prompt_data = json.load(f)

            # TODO: Optionally, validate the structure of prompt_data here
            
            prompts = {}
            for category, data in prompt_data.items():
                prompt = Prompt(category=category, **data)
                prompts[category] = prompt

            return prompts
        except FileNotFoundError:
            logger.error(f"Prompt data file not found at {prompt_data_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format in prompt data file at {prompt_data_path}")
            raise

    def get_prompt(self, style: str, **kwargs) -> Optional[str]:
        """Retrieve a prompt based on the given style.

        Args:
            style (str): The style to retrieve a prompt for.
            **kwargs: Additional options (not currently used).

        Returns:
            Optional[str]: The prompt text, or None if the style is not found.
        """
        prompt_obj = self.prompts.get(style, None)
        if prompt_obj:
            return prompt_obj.get_prompt()
        return None

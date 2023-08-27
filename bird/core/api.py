# core/api.py - Martin Bukowski - 2023-08-26
import json
import requests
import logging
from typing import Optional, Dict

HTTP_OK = 200
BEARER_TOKEN_PREFIX = "Bearer"
JSON_CONTENT_TYPE = "application/json"

class OAIApiException(Exception):
    """Custom exception class for handling OAIApi specific exceptions."""
    pass

class OAIApi:
    """Client class for making requests to the OAI API."""

    def __init__(self, api_key: str, endpoint: str, max_tokens: int):
        """
        Initialize the OAIApi client.

        Args:
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            max_tokens (int): Maximum number of tokens for the generated text.
        """
        self.api_key = api_key
        self.endpoint = endpoint
        self.max_tokens = max_tokens
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_config(cls, endpoint: str, api_key: str, max_tokens: int, **config: Dict[str, Optional[str]]):
        """
        Create an OAIApi instance from a configuration dictionary.

        Args:
            endpoint (str): API endpoint URL.
            api_key (str): API key for authentication.
            max_tokens (int): Maximum number of tokens for the generated text.
            **config (Dict[str, Optional[str]]): Additional optional configuration parameters.

        Returns:
            OAIApi: An instance of the OAIApi class.
        """
        return cls(endpoint=endpoint, api_key=api_key, max_tokens=max_tokens)

    def make_request(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        Make an API request to generate text based on the given prompt.

        Args:
            prompt (str): The text prompt to guide the text generation.
            max_tokens (Optional[int]): Maximum number of tokens for the generated text. Defaults to None.

        Returns:
            str: The generated text.

        Raises:
            OAIApiException: If the API request fails.
        """
        if max_tokens is None:
            max_tokens = self.max_tokens

        headers = {
            "Authorization": f"{BEARER_TOKEN_PREFIX} {self.api_key}",
            "Content-Type": JSON_CONTENT_TYPE
        }
        self.logger.info("Sending Prompt: %s", prompt)
        payload = json.dumps({
            "prompt": prompt,
            "stop": ["\n", '"'],
            "max_tokens": max_tokens
        })
        uri = f"{self.endpoint}/v1/completions"
        response = requests.post(uri, headers=headers, data=payload)

        if response.status_code == HTTP_OK:
            return json.loads(response.text)['choices'][0]['text']
        else:
            raise OAIApiException(f"API request failed with status code {response.status_code}: {response.text}")

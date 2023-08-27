# core/util.py - Martin Bukowski - 2023-08-26
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def validate_config(config: Dict[str, Any]) -> None:
    """Validate the configuration dictionary.

    Args:
        config (Dict[str, Any]): The configuration dictionary to validate.

    Raises:
        ValueError: If the configuration is invalid.
    """
    required_keys = ["endpoint", "api_key", "max_tokens", "bird_data_path", "prompt_data_path"]

    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing '{key}' in configuration.")

    if not isinstance(config['max_tokens'], int):
        raise ValueError("'max_tokens' must be an integer.")

def load_config(config_path: str = "config/config.json") -> Dict[str, Any]:
    """Load and validate configuration settings from a JSON file.

    Args:
        config_path (str, optional): Path to the configuration JSON file. Defaults to 'config/config.json'.

    Returns:
        Dict[str, Any]: Dictionary containing the validated configuration settings.
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        validate_config(config)

        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {config_path}")
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in configuration file at {config_path}")
        raise ValueError(f"Invalid JSON format in configuration file at {config_path}")

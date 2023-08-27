# core/rookery.py - Martin Bukowski - 2023-08-26
import json
import logging
from typing import Dict, Optional
from ..model.bird import Bird

class Rookery:
    def __init__(self, birds: Dict[str, Bird]):
        """Initialize a new Rookery instance."""
        self.birds = birds
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_config(cls, bird_data_path: str, **config: Dict[str, Optional[str]]) -> 'Rookery':
        """Create a new Rookery instance from a configuration file."""
        birds = Rookery.load_birds(bird_data_path)
        return cls(birds=birds)

    @staticmethod
    def load_birds(bird_data_path: str) -> Dict[str, Bird]:
        """Load bird data from a JSON file."""
        try:
            with open(bird_data_path, 'r') as f:
                bird_data = json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to load bird data: {e}")

        birds = {}
        for data in bird_data:
            bird = Bird(**data)
            birds[bird.name] = bird
        return birds

    def get_bird(self, bird_name: str, **kwargs: Optional[Dict]) -> Optional[Bird]:
        """Retrieve a Bird instance by name. Extra kwargs are for future extension."""
        return self.birds.get(bird_name, None)

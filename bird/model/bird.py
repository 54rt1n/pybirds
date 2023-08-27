# model/bird.py - Martin Bukowski - 2023-08-26
import random
from typing import Dict, List, Optional

class Bird:
    def __init__(self, bird_id: int, name: str, species: str, persona: str, 
                 description: str, promptMeta: List[str], physicalDetails: str, 
                 customStyle: Dict[str, List[str]]):
        self.bird_id = bird_id
        self.name = name
        self.species = species
        self.persona = persona
        self.description = description
        self.promptMeta = promptMeta
        self.physicalDetails = physicalDetails
        self.customStyle = customStyle

    def __str__(self):
        return f"{self.name} ({self.species}) - {self.description}"

    def get_custom_style(self, style: str) -> Optional[str]:
        styles = self.customStyle.get(style, None)
        if styles is None:
            return None
        return random.choice(styles)

    def get_prompt(self) -> List[str]:
        return random.choice(self.promptMeta)
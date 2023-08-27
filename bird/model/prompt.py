# model/prompt.py - Martin Bukowski - 2023-08-26
from typing import List
import random

class Prompt:
    def __init__(self, category: str, description: str, prompts: List[str]):
        self.category = category
        self.description = description
        self.prompts = prompts

    def __str__(self):
        return f"{self.category} - {self.description}"

    def get_prompt(self):
        return random.choice(self.prompts)

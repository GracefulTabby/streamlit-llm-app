from typing import NamedTuple


class LLMConfig(NamedTuple):
    model_name: str
    temperature: float
    max_tokens: int

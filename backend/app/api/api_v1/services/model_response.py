from dataclasses import dataclass
from typing import List


@dataclass
class Sentence(object):
    filename: str
    text: str


@dataclass
class WordAndSentences(object):
    word: str
    sentences: List[Sentence]


@dataclass
class ModelResponse:
    topic: str
    words: List[WordAndSentences]

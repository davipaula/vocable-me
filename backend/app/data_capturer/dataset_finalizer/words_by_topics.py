from dataclasses import dataclass


@dataclass
class WordsByTopics:
    topic: str
    word: str
    video_id: str
    audio_file: str
    text: str

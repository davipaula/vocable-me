from dataclasses import dataclass


@dataclass
class SentenceAudioFile:
    video_id: str
    audio_file: str
    text: str

import logging

from fastapi import APIRouter, Depends

from app.api.api_v1.services import dataset_fetcher

words_router = r = APIRouter()

logger = logging.getLogger(__name__)
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s (%(funcName)s@%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


AUDIO_FILES_PATH = "/static/audio/"


@r.get("/topics/")
def get_topics():
    return {
        "topics": [
            "technology",
            "entertainment",
            "design",
            "business",
            "science",
            "global issues",
        ]
    }


@r.get("/sentences/")
def get_captions_containing_most_important_words(
    topic: str, number_of_words: int = 5, number_of_sentences: int = 5,
):
    # TODO implement get words for more than one topic
    return dataset_fetcher.get_sentences(
        topic, number_of_words, number_of_sentences
    )

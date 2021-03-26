import logging

from fastapi import APIRouter, Depends

from db.crud import get_video_captions
from db.session import get_db
from data_capturer.audio_extractor import audio_extractor

import pandas as pd

from model.settings import IMPORTANT_WORDS_PER_TOPIC_PATH

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
    topic: str,
    number_of_words: int = 5,
    number_of_sentences: int = 5,
    db=Depends(get_db),
):
    most_important_words = pd.read_csv(IMPORTANT_WORDS_PER_TOPIC_PATH)
    topic_important_words = most_important_words[
        most_important_words["topic"] == topic
    ]["word"][:number_of_words].tolist()

    logger.info("Getting data from DB")
    video_captions = get_video_captions(
        db, topic_important_words, number_of_sentences
    )
    logger.info("Data retrieved")

    captions_containing_important_words = {"topic": topic, "words": []}
    for word in topic_important_words:
        captions_containing_word = [
            {
                "text": caption.text,
                "audio": AUDIO_FILES_PATH + caption.get_output_filename(),
            }
            for caption in video_captions
            if word in caption.text
        ]

        # TODO filter the number of sentences in the list generation
        captions_containing_word = captions_containing_word[
            :number_of_sentences
        ]

        words_and_sentences = {
            "word": word,
            "sentences": captions_containing_word,
        }

        captions_containing_important_words["words"].append(words_and_sentences)

    logger.info("Finished sentences processing")
    return captions_containing_important_words


@r.get("/audio_extraction")
def audio_extraction():
    audio_extractor.run()

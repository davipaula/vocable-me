import logging
from typing import List

from tqdm import tqdm

from app.data_capturer.audio_extractor.audio_extractor import (
    get_available_audio_files,
    get_processed_video_ids,
)
from app.data_capturer.dataset_finalizer.sentence_audio_file import (
    SentenceAudioFile,
)
from app.data_capturer.dataset_finalizer.words_by_topics import WordsByTopics
from app.db.crud import get_video_captions
from app.db.session import SessionLocal
from app.db.video_caption import VideoCaption
from app.model.important_words import (
    get_important_words_and_topics,
    get_unique_important_words,
)
from app.utils import utils

import pandas as pd

logger = logging.getLogger(__name__)
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s (%(funcName)s@%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def run():
    # TODO this is terrible. We shouldn't be getting anything related to DB connection here
    db = SessionLocal()

    # Get sentences from unique important words
    sentences = get_video_captions(
        db=db,
        words=get_unique_important_words(),
        video_titles=get_processed_video_ids(),
    )

    # Check which sentences were properly processed and prepare result
    available_sentence_audios = get_available_sentence_audios(
        get_available_audio_files(), sentences
    )

    logger.info(f"{len(available_sentence_audios)} available sentence audios")

    # Merge with words + topics
    final_result = merge_words_and_topics(available_sentence_audios)

    # save prepared data as csv
    utils.save_as_json(final_result, "/app/app/data/results/final_dataset.jsonl")


def merge_words_and_topics(
    available_sentence_audios: List[SentenceAudioFile],
) -> List[WordsByTopics]:
    word_and_topics = get_important_words_and_topics()

    logger.info("Merging words and topics")
    final_result = []
    for word_and_topic in tqdm(word_and_topics):
        prepared = [
            WordsByTopics(
                word_and_topic["topic"],
                word_and_topic["word"],
                sentence.video_id,
                sentence.audio_file,
                sentence.text,
            )
            for sentence in available_sentence_audios
            if word_and_topic["word"] in sentence.text.split(" ")
        ]

        final_result.extend(prepared)

    return final_result


def get_available_sentence_audios(
    available_audios, sentences: List[VideoCaption]
) -> List[SentenceAudioFile]:
    available_audios_filenames = [file["filename"] for file in available_audios]
    print(f"Number of filenames {len(available_audios_filenames)}")

    final_results = []
    for sentence in sentences:
        if sentence.get_output_filename() not in available_audios_filenames:
            # logger.info(f"{sentence.get_output_filename()} does not exist")
            continue

        # Get all filenames for this sentence
        sentence_audio_files = [
            SentenceAudioFile(
                sentence.video_id, available_audio["filename"], sentence.text,
            )
            for available_audio in available_audios
            if available_audio["filename"] == sentence.get_output_filename()
        ]

        final_results.extend(sentence_audio_files)

    print(f"Number of final results {len(final_results)}")

    return final_results


if __name__ == "__main__":
    run()

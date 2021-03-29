import logging

from tqdm import tqdm

from data_capturer.audio_extractor.audio_extractor import (
    get_available_audio_files,
    get_processed_video_ids,
)
from db.crud import get_video_captions
from db.session import SessionLocal
from model.important_words import (
    get_important_words_and_topics,
    get_unique_important_words,
)

import pandas as pd

from utils import utils

logger = logging.getLogger(__name__)
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s (%(funcName)s@%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def run():
    # TODO this is terrible. We shouldn't be getting anything related to DB connection here
    db = SessionLocal()

    unique_important_words = get_unique_important_words()
    available_audios = get_available_audio_files()
    available_video_titles = get_processed_video_ids()
    available_audios_filenames = [
        file["filename"] for file in get_available_audio_files()
    ]

    # Get sentences from unique important words
    sentences = get_video_captions(
        db=db, words=unique_important_words, video_titles=available_video_titles
    )

    # Check which sentences were properly processed and prepare result
    available_sentence_audios = get_available_sentence_audios(
        available_audios, available_audios_filenames, sentences
    )

    logger.info(f"{len(available_sentence_audios)} available sentence audios")

    # Merge with words + topics
    word_and_topics = get_important_words_and_topics()
    final_result = []
    logger.info("Processing words")
    for word_and_topic in tqdm(word_and_topics):
        prepared = [
            {**word_and_topic, **sentence}
            for sentence in available_sentence_audios
            if word_and_topic["word"] in sentence["text"]
        ]

        final_result.extend(prepared)

    # save prepared data as csv
    pd.DataFrame(final_result).to_csv(
        "/app/app/data/results/final_dataset.csv", index=False
    )


def get_available_sentence_audios(
    available_audios, available_audios_filenames, sentences
):
    final_results = []
    for sentence in sentences:
        if sentence.get_output_filename() not in available_audios_filenames:
            continue

        # Get all filenames for this sentence
        sentence_audio_files = [
            {
                "video_id": sentence.video_id,
                "audio_file": available_audio["filename"],
                "text": sentence.text,
            }
            for available_audio in available_audios
            if available_audio["video_id"] == sentence.video_id
        ]

        final_results.extend(sentence_audio_files)

    return final_results


if __name__ == "__main__":
    run()

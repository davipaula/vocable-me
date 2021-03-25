import json
import logging
import os
import pickle
from typing import Dict, List

import pandas as pd

from model.settings import (
    TED_RESULTS_PATH,
    TF_IDF_MODEL_PATH,
    IMPORTANT_WORDS_PER_TOPIC_PATH,
    TOPICS,
)
from model.utils import get_captions_text, get_captions_as_json

NUMBER_OF_IMPORTANT_WORDS_PER_TOPIC = 200

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s (%(funcName)s@%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def run():
    """
    Runs TF-IDF for each topic and saves the results as csv
    """
    logger.info("Loading TF-IDF model")
    tf_idf_model = pickle.load(open(TF_IDF_MODEL_PATH, "rb"))
    logger.info("Model loaded")

    logger.info("Processing model and words")

    important_words_per_topic = []
    # TODO topics are hardcoded. Need to get them from the dataset in the future
    for topic in TOPICS:
        important_words = generate_important_words_in_topic(tf_idf_model, topic)

        important_words_per_topic.extend(important_words)
    logger.info("Processing finished")

    logger.info("Saving results")
    pd.DataFrame(important_words_per_topic).to_csv(
        IMPORTANT_WORDS_PER_TOPIC_PATH, index=False
    )
    logger.info("Results saved")


def get_topic_text(topic: str) -> str:
    with open(TED_RESULTS_PATH, "r") as json_file:
        json_lines = list(json_file)

    ted_videos = [json.loads(json_line) for json_line in json_lines]

    # Need to normalize file name and video title. Currently they are different
    # TODO think about how to store the id the right way
    videos_in_topic = [
        video["id"].rsplit("/talks/")[1]
        for video in ted_videos
        if video["topic"] == topic
    ]

    # Need to change `dataset.jsonl` to the right json format (key, value). Currently the key is the file name
    captions = get_captions_as_json()

    # TODO create a Caption data class and add methods to avoid this absurd data manipulation
    captions_from_topic = [
        caption
        for caption in captions
        if caption["title"].rsplit(".en.vtt")[0] in videos_in_topic
    ]

    # TODO check why length of videos_in_topic and captions_from_topic do not match
    # print(len(captions_from_topic))

    topic_text = get_captions_text(captions_from_topic)

    return " ".join(topic_text)


def sort_tf_idf_vectors(tf_idf_topic):
    coocurrence_matrix = tf_idf_topic.tocoo()

    tuples = zip(coocurrence_matrix.col, coocurrence_matrix.data)

    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def get_top_n_words_from_topic(feature_names, sorted_vectors, n: int = 10):
    top_n_vectors = sorted_vectors[:n]

    return {
        feature_names[index]: round(score, 3) for index, score in top_n_vectors
    }


def generate_important_words_in_topic(
    tf_idf_model, topic: str
) -> List[Dict]:
    """
    Runs TF-IDF with the texts of the topic and returns the top N words according to TF-IDF score
    """
    topic_text = get_topic_text(topic)
    tf_idf_topic = tf_idf_model.transform([topic_text])
    sorted_vectors = sort_tf_idf_vectors(tf_idf_topic)
    top_n_words = sorted_vectors[:NUMBER_OF_IMPORTANT_WORDS_PER_TOPIC]

    feature_names = tf_idf_model.get_feature_names()
    return [
        {
            key: value
            for key, value in (
                ("topic", topic),
                ("word", feature_names[index]),
                ("score", round(score, 4)),
            )
        }
        for index, score in top_n_words
    ]


def get_unique_important_words() -> List[str]:
    important_words_df = pd.read_csv(IMPORTANT_WORDS_PER_TOPIC_PATH)

    return important_words_df["word"].unique().tolist()


if __name__ == "__main__":
    run()

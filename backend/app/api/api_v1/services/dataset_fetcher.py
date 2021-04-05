import json
from itertools import groupby
from typing import Dict, List
import random

from app.api.api_v1.services.model_response import (
    ModelResponse,
    Sentence,
    WordAndSentences,
)
from app.utils.utils import get_logger

FINAL_DATASET_PATH = "/app/app/data/results/final_dataset.jsonl"

logger = get_logger()


def get_sentences(topic: str, number_of_words: int, sentences_per_word: int):
    captions = load_dataset()
    important_words = get_n_random_important_words(
        captions, topic, number_of_words
    )
    logger.info(f"Important words {important_words}")
    sentences = _get_sentences(captions, important_words, sentences_per_word)
    logger.info(f"Important sentences {sentences}")

    return _prepare_data(sentences)


def load_dataset():
    with open(FINAL_DATASET_PATH, "r") as json_file:
        json_content = list(json_file)

    return [json.loads(json_line) for json_line in json_content]


def get_n_random_important_words(
    captions: List[Dict], topic: str, number_of_words: int = 5
) -> List[Dict]:
    topic_words = {
        caption["word"] for caption in captions if caption["topic"] == topic
    }

    random_topic_words = random.sample(topic_words, number_of_words)
    # random_topic_words = list(topic_words)[:number_of_words]

    return [{"topic": topic, "word": word} for word in random_topic_words]


def _get_sentences(
    captions: List[Dict],
    words_by_topic: List[Dict],
    number_of_sentences: int = 5,
) -> List[Dict]:
    result = []
    for word_by_topic in words_by_topic:
        sentences_with_word_in_topic = [
            caption
            for caption in captions
            if word_by_topic["topic"] == caption["topic"]
            and word_by_topic["word"] == caption["word"]
        ][:number_of_sentences]

        result.extend(sentences_with_word_in_topic)

    return result


def _prepare_data(dataset_response: List[Dict]):
    captions_grouped_by_topic = [
        {"topic": topic, "topic_captions": list(topic_captions)}
        for topic, topic_captions in groupby(
            dataset_response, lambda caption: caption["topic"]
        )
    ]

    results = []
    for caption_group in captions_grouped_by_topic:
        captions = caption_group["topic_captions"]
        words_grouped_by_topic = [
            {"word": word, "captions": list(topic_captions)}
            for word, topic_captions in groupby(
                captions, lambda caption: caption["word"]
            )
        ]

        word_and_sentences = [
            WordAndSentences(
                word=word_by_topic["word"],
                sentences=_prepare_sentences(word_by_topic["captions"]),
            )
            for word_by_topic in words_grouped_by_topic
        ]

    return ModelResponse(topic=caption_group["topic"], words=word_and_sentences)


def _prepare_sentences(sentences: Dict) -> List[Sentence]:
    return [
        Sentence(sentence["audio_file"], sentence["text"])
        for sentence in sentences
    ]


if __name__ == "__main__":
    print(get_sentences("business", 1, 2))

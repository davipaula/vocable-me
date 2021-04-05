import dataclasses

import pytest

from app.data_capturer.dataset_finalizer.dataset_finalizer import (
    merge_words_and_topics,
)
from app.data_capturer.dataset_finalizer.sentence_audio_file import (
    SentenceAudioFile,
)
from app.data_capturer.dataset_finalizer.words_by_topics import WordsByTopics


@pytest.fixture(autouse=True)
def mock_get_important_words_and_topics(mocker):
    yield mocker.patch(
        "app.data_capturer.dataset_finalizer.dataset_finalizer.get_important_words_and_topics"
    )


def test_merge_words_and_topics_executes():
    available_sentence_audios = [
        SentenceAudioFile("id1", "file1", "text1"),
        SentenceAudioFile("id2", "file2", "text2"),
        SentenceAudioFile("id3", "file3", "text3"),
    ]
    result = merge_words_and_topics(available_sentence_audios)

    assert result is not None


def test_merge_words_and_topics_returns_merged_structure(
    mock_get_important_words_and_topics,
):
    first_sentence = SentenceAudioFile(
        "id1", "file1", "This sentence has word1"
    )
    second_sentence = SentenceAudioFile(
        "id2", "file2", "This sentence has word2"
    )
    third_sentence = SentenceAudioFile(
        "id3", "file3", "This sentence has word3"
    )
    available_sentence_audios = [
        first_sentence,
        second_sentence,
        third_sentence,
    ]
    first_word = {"topic": "topic1", "word": "word1", "score": 0.99}
    second_word = {"topic": "topic1", "word": "word2", "score": 0.88}
    third_word = {"topic": "topic1", "word": "word3", "score": 0.77}
    fourth_word = {"topic": "topic1", "word": "word4", "score": 0.66}
    important_words_and_topics = [
        first_word,
        second_word,
        third_word,
        fourth_word,
    ]

    mock_get_important_words_and_topics.return_value = (
        important_words_and_topics
    )
    expected_result = [
        WordsByTopics(**{**dataclasses.asdict(first_sentence), **first_word}),
        WordsByTopics(**{**dataclasses.asdict(second_sentence), **second_word}),
        WordsByTopics(**{**dataclasses.asdict(third_sentence), **third_word}),
    ]

    result = merge_words_and_topics(available_sentence_audios)

    assert expected_result == result

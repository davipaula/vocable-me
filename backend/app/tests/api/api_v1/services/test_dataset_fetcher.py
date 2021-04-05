from app.api.api_v1.services import dataset_fetcher
from app.api.api_v1.services.model_response import (
    ModelResponse,
    Sentence,
    WordAndSentences,
)


def test_prepare_data_with_one_topic():
    first_audio_filename = "firstAudioLocation.mp3"
    first_sentence_with_first_word = "First sentence with first word"
    first_sentence_first_word = Sentence(
        first_audio_filename, first_sentence_with_first_word,
    )

    second_audio_filename = "secondAudioLocation.mp3"
    second_sentence_with_first_word = "Second sentence with first word"
    second_sentence_first_word = Sentence(
        second_audio_filename, second_sentence_with_first_word,
    )
    first_word = "firstWord"
    first_sentences_with_first_word = WordAndSentences(
        word=first_word,
        sentences=[first_sentence_first_word, second_sentence_first_word],
    )
    topic = "firstTopic"
    words = [first_sentences_with_first_word]
    expected_result = [ModelResponse(topic=topic, words=words)]

    data_input = [
        {
            "topic": topic,
            "word": first_word,
            "video_id": "some_video_id",
            "audio_file": first_audio_filename,
            "text": first_sentence_with_first_word,
        },
        {
            "topic": topic,
            "word": first_word,
            "video_id": "some_video_id",
            "audio_file": second_audio_filename,
            "text": second_sentence_with_first_word,
        },
    ]

    result = dataset_fetcher._prepare_data(data_input)

    assert result == expected_result


def test_prepare_data_with_three_topics():
    first_topic = "topic1"
    first_topic_first_word = "firstWord"
    first_topic_first_audio_filename = "firstAudioLocation.mp3"
    first_topic_first_sentence_with_first_word = (
        "First sentence with first word"
    )
    first_topic_first_sentence_first_word = Sentence(
        first_topic_first_audio_filename,
        first_topic_first_sentence_with_first_word,
    )

    first_topic_second_audio_filename = "secondAudioLocation.mp3"
    first_topic_second_sentence_with_first_word = (
        "Second sentence with first word"
    )
    first_topic_second_sentence_first_word = Sentence(
        first_topic_second_audio_filename,
        first_topic_second_sentence_with_first_word,
    )
    first_topic_first_sentences_with_first_word = WordAndSentences(
        word=first_topic_first_word,
        sentences=[
            first_topic_first_sentence_first_word,
            first_topic_second_sentence_first_word,
        ],
    )
    first_topic_words = [first_topic_first_sentences_with_first_word]

    second_topic = "topic2"
    second_topic_first_word = "secondTopic_firstWord"
    second_topic_first_audio_filename = "secondTopic_firstAudioLocation.mp3"
    second_topic_first_sentence_with_first_word = (
        "Second topic - First sentence with first word"
    )
    second_topic_first_sentence_first_word = Sentence(
        second_topic_first_audio_filename,
        second_topic_first_sentence_with_first_word,
    )

    second_topic_second_audio_filename = "secondTopic_firstAudioLocation.mp3"
    second_topic_second_sentence_with_first_word = (
        "Second topic - Second sentence with first word"
    )
    second_topic_second_sentence_first_word = Sentence(
        second_topic_second_audio_filename,
        second_topic_second_sentence_with_first_word,
    )
    second_topic_second_sentence_first_word = WordAndSentences(
        word=second_topic_first_word,
        sentences=[
            second_topic_first_sentence_first_word,
            second_topic_second_sentence_first_word,
        ],
    )
    second_topic_words = [second_topic_second_sentence_first_word]

    third_topic = "topic3"
    third_topic_first_word = "thirdTopic_firstWord"
    third_topic_first_audio_filename = "thirdTopic_firstAudioLocation.mp3"
    third_topic_first_sentence_with_first_word = (
        "third topic - First sentence with first word"
    )
    third_topic_first_sentence_first_word = Sentence(
        third_topic_first_audio_filename,
        third_topic_first_sentence_with_first_word,
    )

    third_topic_second_sentence_first_word = WordAndSentences(
        word=third_topic_first_word,
        sentences=[third_topic_first_sentence_first_word,],
    )
    third_topic_words = [third_topic_second_sentence_first_word]

    expected_result = [
        ModelResponse(topic=first_topic, words=first_topic_words),
        ModelResponse(topic=second_topic, words=second_topic_words),
        ModelResponse(topic=third_topic, words=third_topic_words),
    ]

    data_input = [
        {
            "topic": first_topic,
            "word": first_topic_first_word,
            "video_id": "some_video_id",
            "audio_file": first_topic_first_audio_filename,
            "text": first_topic_first_sentence_with_first_word,
        },
        {
            "topic": first_topic,
            "word": first_topic_first_word,
            "video_id": "some_video_id",
            "audio_file": first_topic_second_audio_filename,
            "text": first_topic_second_sentence_with_first_word,
        },
        {
            "topic": second_topic,
            "word": second_topic_first_word,
            "video_id": "some_video_id",
            "audio_file": second_topic_first_audio_filename,
            "text": second_topic_first_sentence_with_first_word,
        },
        {
            "topic": second_topic,
            "word": second_topic_first_word,
            "video_id": "some_video_id",
            "audio_file": second_topic_second_audio_filename,
            "text": second_topic_second_sentence_with_first_word,
        },
        {
            "topic": third_topic,
            "word": third_topic_first_word,
            "video_id": "some_video_id",
            "audio_file": third_topic_first_audio_filename,
            "text": third_topic_first_sentence_with_first_word,
        },
    ]

    result = dataset_fetcher._prepare_data(data_input)

    assert result == expected_result


def test_prepare_data_with_two_words_and_one_topic():
    first_topic = "topic1"
    first_topic_first_word = "firstWord"
    first_topic_first_audio_filename = "firstAudioLocation.mp3"
    first_topic_first_sentence_with_first_word = (
        "First sentence with first word"
    )
    first_topic_first_sentence_first_word = Sentence(
        first_topic_first_audio_filename,
        first_topic_first_sentence_with_first_word,
    )

    first_topic_second_audio_filename = "secondAudioLocation.mp3"
    first_topic_second_sentence_with_first_word = (
        "Second sentence with first word"
    )
    first_topic_second_sentence_first_word = Sentence(
        first_topic_second_audio_filename,
        first_topic_second_sentence_with_first_word,
    )

    first_topic_second_word = "secondWord"
    first_topic_second_word_audio_filename = "thirdAudioLocation.mp3"
    first_topic_first_sentence_with_second_word = (
        "First sentence with second word"
    )
    first_topic_first_sentence_second_word = Sentence(
        first_topic_second_word_audio_filename,
        first_topic_first_sentence_with_second_word,
    )

    first_topic_sentences_with_first_word = WordAndSentences(
        word=first_topic_first_word,
        sentences=[
            first_topic_first_sentence_first_word,
            first_topic_second_sentence_first_word,
        ],
    )

    first_topic_sentences_with_second_word = WordAndSentences(
        word=first_topic_second_word,
        sentences=[first_topic_first_sentence_second_word],
    )
    first_topic_words = [
        first_topic_sentences_with_first_word,
        first_topic_sentences_with_second_word,
    ]

    expected_result = [
        ModelResponse(topic=first_topic, words=first_topic_words),
    ]

    data_input = [
        {
            "topic": first_topic,
            "word": first_topic_first_word,
            "video_id": "some_video_id",
            "audio_file": first_topic_first_audio_filename,
            "text": first_topic_first_sentence_with_first_word,
        },
        {
            "topic": first_topic,
            "word": first_topic_first_word,
            "video_id": "some_video_id",
            "audio_file": first_topic_second_audio_filename,
            "text": first_topic_second_sentence_with_first_word,
        },
        {
            "topic": first_topic,
            "word": first_topic_second_word,
            "video_id": "some_video_id",
            "audio_file": first_topic_second_word_audio_filename,
            "text": first_topic_first_sentence_with_second_word,
        },
    ]

    result = dataset_fetcher._prepare_data(data_input)

    assert result == expected_result


def test_prepare_data_with_two_topics_different_words():
    first_topic = "topic1"
    first_topic_first_word = "firstWord"
    first_topic_first_audio_filename = "firstAudioLocation.mp3"
    first_topic_first_sentence_with_first_word = (
        "First sentence with first word"
    )
    first_topic_first_sentence_first_word = Sentence(
        first_topic_first_audio_filename,
        first_topic_first_sentence_with_first_word,
    )

    first_topic_second_audio_filename = "secondAudioLocation.mp3"
    first_topic_second_sentence_with_first_word = (
        "Second sentence with first word"
    )
    first_topic_second_sentence_first_word = Sentence(
        first_topic_second_audio_filename,
        first_topic_second_sentence_with_first_word,
    )

    first_topic_second_word = "secondWord"
    first_topic_second_word_audio_filename = "thirdAudioLocation.mp3"
    first_topic_first_sentence_with_second_word = (
        "First sentence with second word"
    )
    first_topic_first_sentence_second_word = Sentence(
        first_topic_second_word_audio_filename,
        first_topic_first_sentence_with_second_word,
    )

    first_topic_sentences_with_first_word = WordAndSentences(
        word=first_topic_first_word,
        sentences=[
            first_topic_first_sentence_first_word,
            first_topic_second_sentence_first_word,
        ],
    )

    first_topic_sentences_with_second_word = WordAndSentences(
        word=first_topic_second_word,
        sentences=[first_topic_first_sentence_second_word],
    )
    first_topic_words = [
        first_topic_sentences_with_first_word,
        first_topic_sentences_with_second_word,
    ]

    second_topic = "topic2"
    second_topic_first_word = "secondTopic_firstWord"
    second_topic_first_audio_filename = "secondTopic_firstAudioLocation.mp3"
    second_topic_first_sentence_with_first_word = (
        "Second topic - First sentence with first word"
    )
    second_topic_first_sentence_first_word = Sentence(
        second_topic_first_audio_filename,
        second_topic_first_sentence_with_first_word,
    )

    second_topic_second_audio_filename = "secondTopic_firstAudioLocation.mp3"
    second_topic_second_sentence_with_first_word = (
        "Second topic - Second sentence with first word"
    )
    second_topic_second_sentence_first_word = Sentence(
        second_topic_second_audio_filename,
        second_topic_second_sentence_with_first_word,
    )
    second_topic_second_sentence_first_word = WordAndSentences(
        word=second_topic_first_word,
        sentences=[
            second_topic_first_sentence_first_word,
            second_topic_second_sentence_first_word,
        ],
    )

    second_topic_second_word = "secondTopic_secondWord"
    second_topic_third_audio_filename = "secondTopic_thirdAudioLocation.mp3"
    second_topic_first_sentence_with_second_word = (
        "Second topic - First sentence with second word"
    )
    second_topic_first_sentence_second_word = Sentence(
        second_topic_third_audio_filename,
        second_topic_first_sentence_with_second_word,
    )
    second_topic_first_sentence_second_word = WordAndSentences(
        word=second_topic_second_word,
        sentences=[second_topic_first_sentence_second_word,],
    )

    second_topic_words = [
        second_topic_second_sentence_first_word,
        second_topic_first_sentence_second_word,
    ]

    expected_result = [
        ModelResponse(topic=first_topic, words=first_topic_words),
        ModelResponse(topic=second_topic, words=second_topic_words),
    ]

    data_input = [
        {
            "topic": first_topic,
            "word": first_topic_first_word,
            "video_id": "some_video_id",
            "audio_file": first_topic_first_audio_filename,
            "text": first_topic_first_sentence_with_first_word,
        },
        {
            "topic": first_topic,
            "word": first_topic_first_word,
            "video_id": "some_video_id",
            "audio_file": first_topic_second_audio_filename,
            "text": first_topic_second_sentence_with_first_word,
        },
        {
            "topic": first_topic,
            "word": first_topic_second_word,
            "video_id": "some_video_id",
            "audio_file": first_topic_second_word_audio_filename,
            "text": first_topic_first_sentence_with_second_word,
        },
        {
            "topic": second_topic,
            "word": second_topic_first_word,
            "video_id": "some_video_id",
            "audio_file": second_topic_first_audio_filename,
            "text": second_topic_first_sentence_with_first_word,
        },
        {
            "topic": second_topic,
            "word": second_topic_first_word,
            "video_id": "some_video_id",
            "audio_file": second_topic_second_audio_filename,
            "text": second_topic_second_sentence_with_first_word,
        },
        {
            "topic": second_topic,
            "word": second_topic_second_word,
            "video_id": "some_video_id",
            "audio_file": second_topic_third_audio_filename,
            "text": second_topic_first_sentence_with_second_word,
        },
    ]

    result = dataset_fetcher._prepare_data(data_input)

    assert result == expected_result

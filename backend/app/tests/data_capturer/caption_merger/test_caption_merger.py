import pytest

from app.data_capturer.caption_merger.caption_merger import merge_captions


def test_caption_merger():
    sentences = [
        "This is a text with a punctuation.",
        "This is a text without punctuation",
        "and this is the continuation of the text",
        "and this is the final part.",
        "This is the final U.K. sentence, without punctuation",
    ]

    result = merge_captions(sentences)

    assert result is not None

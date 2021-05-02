import pytest

from app.data_capturer.caption_merger.caption_merger import merge_captions


def test_caption_merger():
    sentences = [
        {
            "start": "00:00:15.330",
            "end": "00:00:17.330",
            "text": "I've spent the last decade",
        },
        {
            "start": "00:00:17.330",
            "end": "00:00:20.330",
            "text": "subjecting myself to pain and humiliation,",
        },
        {
            "start": "00:00:20.330",
            "end": "00:00:22.330",
            "text": "hopefully for a good cause,",
        },
        {
            "start": "00:00:22.330",
            "end": "00:00:25.330",
            "text": "which is self-improvement.",
        },
        {
            "start": "00:00:25.330",
            "end": "00:00:27.330",
            "text": "And I've done this in three parts.",
        },
        {
            "start": "00:00:27.330",
            "end": "00:00:30.330",
            "text": "So first I started with the mind.",
        },
        {
            "start": "00:00:30.330",
            "end": "00:00:34.330",
            "text": "And I decided to try to get smarter",
        },
        {
            "start": "00:00:34.330",
            "end": "00:00:36.330",
            "text": "by reading the entire Encyclopedia Britannica",
        },
        {
            "start": "00:00:36.330",
            "end": "00:00:38.330",
            "text": "from A to Z --",
        },
        {
            "start": "00:00:38.330",
            "end": "00:00:41.330",
            "text": 'or, more precisely, from "a-ak" to "Zywiec."',
        },
    ]
    expected_result = [
        {
            "start": "00:00:15.330",
            "end": "00:00:25.330",
            "text": "I've spent the last decade subjecting myself to pain and humiliation, hopefully for a good cause, which is self-improvement.",
        },
        {
            "start": "00:00:25.330",
            "end": "00:00:27.330",
            "text": "And I've done this in three parts.",
        },
        {
            "start": "00:00:27.330",
            "end": "00:00:30.330",
            "text": "So first I started with the mind.",
        },
        {
            "start": "00:00:30.330",
            "end": "00:00:41.330",
            "text": 'And I decided to try to get smarter by reading the entire Encyclopedia Britannica from A to Z -- or, more precisely, from "a-ak" to "Zywiec."',
        },
    ]

    result = merge_captions(sentences)

    assert result == expected_result

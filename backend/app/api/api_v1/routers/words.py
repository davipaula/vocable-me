from fastapi import APIRouter, Depends

from db.crud import get_video_captions
from model import tf_idf

words_router = r = APIRouter()


@r.get("/words/")
def by_topic(topic: str, number_of_words: int):
    most_important_words = tf_idf.run(topic, number_of_words)

    return {"topic": topic, "words": most_important_words}


@r.get("/sentences/")
def get_captions_containing_most_important_words(
    topic: str, number_of_words: int = 5, number_of_sentences: int = 5
):
    most_important_words = tf_idf.run(topic, number_of_words)

    query_result = get_video_captions(most_important_words, limit=1)

    captions_from_words = {"topic": topic, "words": []}
    for word in most_important_words:
        captions_containing_word = [
            # TODO clean text in the dataset ingestion
            caption[1]["text"].replace("\n", " ")
            for caption in query_result
            if word in caption[1]["text"]
        ]

        # TODO filter the number of sentences in the list generation
        captions_containing_word = captions_containing_word[:number_of_sentences]

        words_and_sentences = {"word": word, "sentences": captions_containing_word}

        captions_from_words["words"].append(words_and_sentences)

    return captions_from_words

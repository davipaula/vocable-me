from typing import List

from app.db.crud import get_video_captions
from app.db.session import SessionLocal
from app.db.video_caption import VideoCaption

from app.model.important_words import get_unique_important_words


def select_video_captions() -> List[VideoCaption]:
    """
    It is not feasible to process and store **all** the audios - it can easily reach 30+ Gb.

    We need to select a set of audios and process them. Initially, we will do it for:
    - Words per topic: 200
    - Sentences per word: 10
    - Number of topics: 5

    In total, we will end up with a maximum of 200 * 10 * 5 = 10,000 filename files
    """
    # We already have saved the top 200 most important words per topic
    important_words = get_unique_important_words()[:70]

    sentences_per_word = 5

    # this is terrible. We shouldn't be getting anything related to DB connection here
    db = SessionLocal()

    return get_video_captions(db, important_words, sentences_per_word)


if __name__ == "__main__":
    for caption in select_video_captions()[:5]:
        print(f"start_time: {caption.start_time}, text: {caption.text} \n")

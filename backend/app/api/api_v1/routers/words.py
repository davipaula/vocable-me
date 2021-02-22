from fastapi import APIRouter, Depends

from db.crud import get_video_captions
from db.session import get_db
from model import tf_idf

words_router = r = APIRouter()


@r.get("/topics/{topic}/{number_of_words}")
def by_topic(topic: str, number_of_words: int):
    most_important_words = tf_idf.run(topic, number_of_words)

    return {"topic": topic, "words": most_important_words}


@r.get("/topic/videos/")
def get_videos_with_words(db=Depends(get_db)):
    topic = "business"
    word = "company"

    return {"value": get_video_captions(word, limit=1)}

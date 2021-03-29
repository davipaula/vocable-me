import logging
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session


from . import models, schemas
from core.security import get_password_hash
from .video_caption import VideoCaption

logger = logging.getLogger(__name__)
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s (%(funcName)s@%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.NOTSET, format=LOG_FORMAT)


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> List[schemas.UserOut]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_video_caption(db: Session, video_caption: schemas.VideoCaption):
    db_video_caption = models.RawVideoCaption(
        title=video_caption.title, caption=video_caption.caption
    )
    db.add(db_video_caption)
    db.commit()
    db.refresh(db_video_caption)
    return db_video_caption


def get_video_captions(
    db: Session,
    words: List[str],
    sentences_per_video: int = 5,
    videos_per_word: int = 5,
    video_titles: List[str] = None,
) -> List[VideoCaption]:
    # TODO fix this terrible query creation. There should be a clever way to do it
    base_query = """select * from (
        select
        title,
        captions,
        row_number() over (partition by title) as rowNumber 
        from video_caption, jsonb_array_elements(caption) as captions """

    where_query = f"""
    where
        captions->>'text' similar to '%({'|'.join(words)})%'
        and title = video_caption.title
        and caption = video_caption.caption """

    if video_titles is not None:
        where_query += f" and title in ({','.join(video_titles)})"

    end_query = f"""
    ) p
    where rowNumber <= {sentences_per_video}
    limit {sentences_per_video * videos_per_word * len(words)};
    """

    query = db.execute(base_query + where_query + end_query)

    query_results = query.fetchall()

    logger.info(f"{len(query_results)} results retrieved")

    # TODO investigate a better way to instantiate this object
    return [
        VideoCaption(
            result[0], result[1]["text"], result[1]["start"], result[1]["end"]
        )
        for result in query_results
    ]


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
    db: Session, user_id: int, user: schemas.UserEdit
) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

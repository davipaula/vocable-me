import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
import psycopg2


from . import models, schemas
from core.security import get_password_hash

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
) -> t.List[schemas.UserOut]:
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
    db_video_caption = models.VideoCaption(
        title=video_caption.title, caption=video_caption.caption
    )
    db.add(db_video_caption)
    db.commit()
    db.refresh(db_video_caption)
    return db_video_caption


def get_video_captions(
    db: Session, words: t.List[str], sentences_per_video: int = 5
):
    query = db.execute(
        f"select * from ( "
        f"select "
        f"     title,	"
        f"     captions,"
        f"     row_number() over (partition by title) as rowNumber "
        f"from video_caption,"
        f"     jsonb_array_elements(caption) as captions "
        f"where "
        f"    captions->>'text' similar to '%({'|'.join(words)})%'"
        f"and title = video_caption.title and caption = video_caption.caption"
        f") p "
        f"where rowNumber <= {sentences_per_video};"
    )

    return query.fetchall()


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

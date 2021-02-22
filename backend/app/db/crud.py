import logging

import sqlalchemy
from fastapi import HTTPException, status
from sqlalchemy import String, cast, type_coerce
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import JSONB
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
    word: str, skip: int = 0, limit: int = 10
) -> t.List[schemas.VideoCaption]:
    con = psycopg2.connect(
        host="postgres",
        database="postgres",
        user="postgres",
        password="password",
    )

    cur = con.cursor()

    # execute query
    cur.execute(
        f"select title, captions from video_caption, jsonb_array_elements(caption) as captions where captions->>'text' like '%{word}%';"
    )

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows

    query = (
        db.query(models.VideoCaption).filter(
            models.VideoCaption.caption["text"].contains(
                '"for them not to suffer"'
            )
        )
        # .offset(skip)
        # .limit(1)
        # .all()
    )

    return str(
        query.statement.compile(
            dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
        )
    )

    return db.execute(
        'select title from video_caption where caption @> \'[{"text":"for them not to suffer"}]\';'
    )
    # return "Does it still work?"
    # return db.engine.execute("select * from video_caption limit 1;")


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

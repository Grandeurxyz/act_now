from sqlalchemy import select
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.auth.models import User
from app.auth.schemas import UserRegister


password_hash = PasswordHash.recommended()


def register_user(data: UserRegister, db: Session) -> User:
    existing_user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if existing_user:
        raise ValueError("Email is already registered")

    user = User(
        name=data.name,
        email=str(data.email).lower(),
        password_hash=password_hash.hash(data.password),
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise

    return user
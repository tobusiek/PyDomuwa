from sqlmodel import Session, select

from domuwa.auth.models import UserDb


def get_user(username: str, session: Session):
    return session.exec(select(UserDb).where(UserDb.login == username)).first()  # type: ignore

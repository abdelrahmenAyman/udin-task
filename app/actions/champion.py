from sqlmodel import Session, select

from app.errors import RecordDoesNotExist
from app.models import db as models


class Champion:
    @classmethod
    async def create(cls, name: str, session: Session) -> models.Champion:
        champion = models.Champion(name=name)
        session.add(champion)
        session.flush()
        return champion

    @classmethod
    async def get_by_id(cls, id: int, session: Session) -> models.Champion:
        champion = session.get(models.Champion, id)
        if not champion:
            raise RecordDoesNotExist(f"Champion with ID {id} does not exist")
        return champion

    @classmethod
    async def list(cls, session: Session) -> list[models.Champion]:
        return list(session.exec(select(models.Champion)).all())

    @classmethod
    async def update(cls, id: int, name: str, session: Session) -> models.Champion:
        champion = await cls.get_by_id(id, session)
        champion.name = name
        session.add(champion)
        return champion

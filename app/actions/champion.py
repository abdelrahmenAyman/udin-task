from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app import models
from app.actions.base_stats import BaseStats
from app.errors import RecordAlreadyExists, RecordDoesNotExist
from app.schemas.champion import ChampionCreate, ChampionUpdate


class Champion:
    @classmethod
    async def create(cls, name: str, session: Session) -> models.Champion:
        try:
            champion = models.Champion(name=name)
            session.add(champion)
            session.flush()
            return champion
        except IntegrityError:
            raise RecordAlreadyExists(f"Champion with name {name} already exists.")

    @classmethod
    async def create_with_base_stats(cls, data: ChampionCreate, session: Session) -> models.Champion:
        champion = await cls.create(data.name, session)
        await BaseStats.create(champion_id=champion.id, data=data.base_stats, session=session)
        session.add(champion)
        session.commit()
        session.refresh(champion)
        return champion

    @classmethod
    async def get_by_id(cls, id: int, session: Session) -> models.Champion:
        champion = session.get(models.Champion, id)
        if not champion:
            raise RecordDoesNotExist(f"Champion with ID {id} does not exist")
        return champion

    @classmethod
    async def list(
        cls,
        session: Session,
        offset: int = 0,
        limit: int = 10,
    ) -> list[models.Champion]:
        return list(session.exec(select(models.Champion).offset(offset).limit(limit)).all())

    @classmethod
    async def update(cls, id: int, data: ChampionUpdate, session: Session) -> models.Champion:
        champion = await cls.get_by_id(id, session)
        for attr, value in data.model_dump(exclude_unset=True).items():
            setattr(champion, attr, value)

        session.add(champion)
        session.commit()
        session.refresh(champion)
        return champion

    @classmethod
    async def delete(cls, id, session: Session):
        champion = await cls.get_by_id(id, session)
        session.delete(champion)
        session.commit()

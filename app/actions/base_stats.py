from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select

from app import models
from app.errors import RecordDoesNotExist
from app.schemas.base_stats import BaseStatsCreate, BaseStatsUpdate


class BaseStats:
    @classmethod
    async def create(cls, champion_id: int, data: BaseStatsCreate, session: Session) -> models.BaseStats:
        stats = models.BaseStats(champion_id=champion_id, **data.model_dump())
        try:
            session.add(stats)
            session.flush()
        except IntegrityError:
            raise RecordDoesNotExist(f"Champion with ID {champion_id} does not exist.")
        return stats

    @classmethod
    async def get_by_champion_id(cls, champion_id: int, session: Session) -> models.BaseStats:
        try:
            stats = session.exec(select(models.BaseStats).where(models.BaseStats.champion_id == champion_id)).one()
        except NoResultFound:
            raise RecordDoesNotExist(f"Base stats for champion with ID {champion_id} does not exist.")
        return stats

    @classmethod
    async def update(cls, champion_id: int, data: BaseStatsUpdate, session: Session) -> models.BaseStats:
        stats = await cls.get_by_champion_id(champion_id=champion_id, session=session)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(stats, key, value)

        session.add(stats)
        session.commit()
        session.refresh(stats)
        return stats

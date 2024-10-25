from pydantic import BaseModel

from app.schemas.base_stats import BaseStatsCreate, BaseStatsRead


class ChampionCreate(BaseModel):
    name: str
    base_stats: BaseStatsCreate


class ChampionUpdate(BaseModel):
    name: str | None = None


class ChampionRead(BaseModel):
    id: int
    name: str
    base_stats: BaseStatsRead

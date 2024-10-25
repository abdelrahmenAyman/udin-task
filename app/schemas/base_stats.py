from pydantic import BaseModel


class BaseStatsCreate(BaseModel):
    health: int
    mana: int
    attack_damage: int
    armor: int


class BaseStatsUpdate(BaseModel):
    health: int | None = None
    mana: int | None = None
    attack_damage: int | None = None
    armor: int | None = None


class BaseStatsRead(BaseModel):
    id: int
    health: int
    mana: int
    attack_damage: int
    armor: int

from sqlmodel import Field, Relationship, SQLModel


class Base(SQLModel):
    __abstract__ = True
    __table_args__ = {"schema": "my_schema"}


class Champion(Base, table=True):
    """This model represents a champion in League of legends game (look it up :D)"""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    base_stats: "BaseStats" = Relationship(back_populates="champion", cascade_delete=True)


class BaseStats(Base, table=True):
    """A simplified version of a champion's base stats"""

    id: int = Field(default=None, primary_key=True)
    health: int
    mana: int
    attack_damage: int
    armor: int

    champion_id: int | None = Field(default=None, foreign_key="my_schema.champion.id")
    champion: Champion = Relationship(back_populates="base_stats", sa_relationship_kwargs={"uselist": False})

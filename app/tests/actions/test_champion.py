import pytest
from sqlmodel import select

from app import actions, models
from app.errors import RecordDoesNotExist
from app.schemas.base_stats import BaseStatsCreate
from app.schemas.champion import ChampionCreate, ChampionUpdate


@pytest.mark.asyncio
class TestChampion:
    async def test_create_champion(self, session):
        champion = await actions.Champion.create(name="Sylas", session=session)
        session.commit()
        session.expire(champion)

        fetched_champion = session.get(models.Champion, champion.id)

        assert fetched_champion.name == "Sylas"
        assert fetched_champion.id == champion.id
        assert fetched_champion.base_stats is None

    async def test_get_champion_by_id_success(self, session, champions):
        session.add(champions[0])
        fetched_champion = await actions.Champion.get_by_id(id=champions[0].id, session=session)

        assert fetched_champion.name == champions[0].name
        assert fetched_champion.id == champions[0].id

    async def test_get_champion_by_id_does_not_exist(self, session, champions):
        with pytest.raises(RecordDoesNotExist):
            await actions.Champion.get_by_id(id=100, session=session)

    async def test_list_champions(self, session, champions):
        fetched_champions = await actions.Champion.list(session=session)

        assert len(fetched_champions) == len(champions)
        for fetched, champion in zip(fetched_champions, champions):
            assert fetched.name == champion.name
            assert fetched.id == champion.id

    async def test_list_champions_with_offset_and_limit(self, session, champions):
        fetched_champions = await actions.Champion.list(offset=1, limit=2, session=session)

        assert len(fetched_champions) == 2
        for fetched, champion in zip(fetched_champions, champions[1:]):
            assert fetched.name == champion.name
            assert fetched.id == champion.id

    async def test_update_champion(self, session, champions):
        champion = await actions.Champion.update(
            id=champions[0].id, data=ChampionUpdate(name="Malphite"), session=session
        )
        session.commit()
        session.expire(champion)

        fetched_champion = session.get(models.Champion, champions[0].id)
        assert fetched_champion.id == champions[0].id
        assert fetched_champion.name == "Malphite"

    async def test_update_champion_invalid_id(self, session, champions):
        with pytest.raises(RecordDoesNotExist):
            await actions.Champion.update(id=100, data=ChampionUpdate(name="Malphite"), session=session)

    async def test_update_champion_with_empty_data(self, session, champions):
        champion = await actions.Champion.update(id=champions[0].id, data=ChampionUpdate(), session=session)
        session.commit()
        session.expire(champion)

        fetched_champion = session.get(models.Champion, champions[0].id)
        assert fetched_champion.name == champions[0].name

    async def test_delete_champion_valid_id(self, session, champions):
        await actions.Champion.delete(id=champions[0].id, session=session)

        champions_list = session.exec(select(models.Champion).where(models.Champion.id == champions[0].id)).all()
        stats_list = session.exec(
            select(models.BaseStats).where(models.BaseStats.champion_id == champions[0].id)
        ).all()

        assert len(champions_list) == 0
        assert len(stats_list) == 0

    async def test_delete_champion_invalid_id(self, session):
        with pytest.raises(RecordDoesNotExist):
            await actions.Champion.delete(id=100, session=session)

    async def create_champion_with_base_stats(self, session):
        data = ChampionCreate(
            name="Sylas", base_stats=BaseStatsCreate(health=500, mana=240, attack_damage=65, armor=35)
        )
        champion = await actions.Champion.create_with_base_stats(data=data, session=session)
        session.commit()
        session.expire(champion)

        fetched_champion = session.get(models.Champion, champion.id)

        assert fetched_champion.name == "Sylas"
        assert fetched_champion.base_stats.health == 500
        assert fetched_champion.base_stats.mana == 240

import pytest

from app import actions, models
from app.errors import RecordDoesNotExist
from app.schemas.base_stats import BaseStatsCreate, BaseStatsUpdate


@pytest.mark.asyncio
class TestBaseStats:
    async def test_create_with_valid_champion_id(self, session, champions):
        stats = await actions.BaseStats.create(
            champion_id=champions[0].id,
            data=BaseStatsCreate(health=500, mana=240, attack_damage=65, armor=35),
            session=session,
        )
        session.commit()
        session.expire(stats)
        fetched_stats = session.get(models.BaseStats, stats.id)

        assert fetched_stats.id == stats.id
        assert fetched_stats.champion_id == champions[0].id
        assert fetched_stats.health == 500
        assert fetched_stats.mana == 240
        assert fetched_stats.attack_damage == 65
        assert fetched_stats.armor == 35

    async def test_create_with_invalid_champion_id(self, session, champions):
        with pytest.raises(RecordDoesNotExist):
            await actions.BaseStats.create(
                champion_id=100,
                data=BaseStatsCreate(health=500, mana=240, attack_damage=65, armor=35),
                session=session,
            )

    async def test_get_stats_by_champion_id(self, session, champions):
        stats = await actions.BaseStats.get_by_champion_id(champion_id=champions[0].id, session=session)
        session.add(champions[0])

        assert stats.id == champions[0].base_stats.id

    async def test_get_stats_by_invalid_champion_id(self, session):
        with pytest.raises(RecordDoesNotExist):
            await actions.BaseStats.get_by_champion_id(champion_id=100, session=session)

    async def test_update_champion_stats_with_valid_champion_id(self, session, champions):
        stats = await actions.BaseStats.update(
            champion_id=champions[0].id, data=BaseStatsUpdate(health=350), session=session
        )
        session.add(champions[0])
        session.commit()
        session.expire(stats)

        updated_stats = session.get(models.BaseStats, stats.id)

        assert updated_stats.health == 350

        update_stats_dict = updated_stats.model_dump()
        for field, original_value in champions[0].base_stats.model_dump().items():
            if field != "health":
                assert update_stats_dict[field] == original_value

    async def test_update_champion_stats_with_invalid_champion_id(self, session):
        with pytest.raises(RecordDoesNotExist):
            await actions.BaseStats.update(champion_id=100, data=BaseStatsUpdate(health=350), session=session)

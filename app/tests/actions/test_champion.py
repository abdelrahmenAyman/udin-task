import pytest

from app import actions
from app.errors import RecordDoesNotExist
from app.models import db as models


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

    async def test_update_champion(self, session, champions):
        champion = await actions.Champion.update(id=champions[0].id, name="Malphite", session=session)
        session.commit()
        session.expire(champion)

        fetched_champion = session.get(models.Champion, champions[0].id)
        assert fetched_champion.id == champions[0].id
        assert fetched_champion.name == "Malphite"

import pytest

from app import models


@pytest.mark.asyncio
class TestChampion:
    url = "/champions/"

    async def test_create_champion(self, client, session):
        data = {
            "name": "Sylas",
            "base_stats": {
                "health": 500,
                "mana": 240,
                "attack_damage": 65,
                "armor": 35,
            },
        }
        response = client.post(self.url, json=data)
        print(response.json())

        assert response.status_code == 201
        assert "name" in response.json()
        assert "base_stats" in response.json()

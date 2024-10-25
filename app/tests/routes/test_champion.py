import pytest


@pytest.mark.asyncio
class TestChampion:
    url = "/champions"

    async def test_create_champion(self, client):
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
        json_response = response.json()

        assert response.status_code == 201
        assert "name" in json_response
        assert "base_stats" in json_response

    async def test_list_champions(self, client, champions):
        response = client.get(self.url)
        json_response = response.json()
        print(json_response)

        assert response.status_code == 200
        assert isinstance(json_response, list)
        assert "name" in json_response[0]
        assert "base_stats" in json_response[0]

    async def test_list_champions_offset_lt_zero(self, client, champions):
        response = client.get(f"{self.url}?offset=-1&limit=10")

        assert response.status_code == 422

    async def test_list_champions_limit_gt_100(self, client, champions):
        response = client.get(f"{self.url}?offset=0&limit=101")

        assert response.status_code == 422

    async def test_reach_champion_success(self, client, session, champions):
        session.add(champions[0])
        response = client.get(f"{self.url}/{champions[0].id}/")
        json_response = response.json()

        assert response.status_code == 200
        assert json_response["name"] == champions[0].name
        assert json_response["base_stats"]["id"] == champions[0].base_stats.id

    async def test_read_champion_does_not_exist(self, client, champions):
        response = client.get(f"{self.url}/100/")

        assert response.status_code == 404

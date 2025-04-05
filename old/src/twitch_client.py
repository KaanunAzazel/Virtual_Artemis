import aiohttp
import asyncio
import os

VTUBER_TAG_ID = '6ea6bca4-4712-4ab9-a906-e3336a9d8039'
ID_CLIENT = os.getenv('ID_CLIENT')
SECRET_CLIENT = os.getenv('SECRET_KEY')


class TwitchClient:
    def __init__(self):
        self.token = None

    async def authenticate(self):
        # Test created to validate the authentication token
        url = f'https://id.twitch.tv/oauth2/token?client_id={ID_CLIENT}&client_secret={SECRET_CLIENT}&grant_type=client_credentials'
        # Use aiohttp to make an asynchronous POST request
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as resp:
                result = await resp.json()
                self.token = result['access_token']

    async def get_vtuber_streams(self):
        headers = {
            'Client-ID': ID_CLIENT,
            'Authorization': f'Bearer {self.token}'
        }

        url = f'https://api.twitch.tv/helix/streams?first=10&tag_id={VTUBER_TAG_ID}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                data = await resp.json()
                return data.get("data", [])

    async def get_all_tags_id(self):
        url = f'https://api.twitch.tv/helix/tags/streams'
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Client-Id": ID_CLIENT
        }

        list_tags = ["VtuberBR", "Vtuber", "Português", "pt", "Brasil"]
        tag_dict = {}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                data = await resp.json()

                for tag in data["data"]:
                    if tag["name"] in list_tags:
                        tag_dict[tag["name"]] = tag["tag_id"]

                pagination = data.get("pagination", {})
                cursor = pagination.get("cursor")
                if cursor:
                    url = f"https://api.twitch.tv/helix/tags/streams?first=100&after={cursor}"
                else:
                    url = None

        return tag_dict

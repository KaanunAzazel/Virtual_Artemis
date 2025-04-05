import pytest
from unittest.mock import AsyncMock, patch
from src.twitch_client import TwitchClient


@pytest.mark.asyncio
async def test_authenticate_token_correctly():
    mock_token = "mock_token"

    # Cria o mock da resposta
    fake_response = AsyncMock()
    fake_response.__aenter__.return_value.json.return_value = {
        "access_token": mock_token}

    # Agora sim, esse mock funciona com 'async with'
    with patch("aiohttp.ClientSession.post", return_value=fake_response):
        client = TwitchClient()
        await client.authenticate()

        assert client.token == mock_token

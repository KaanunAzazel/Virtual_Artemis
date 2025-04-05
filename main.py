import asyncio
from src.twitch_client import TwitchClient


async def main():
    twitch = TwitchClient()
    await twitch.authenticate()
    streams = await twitch.get_vtuber_streams()

    if len(streams) > 0:
        for stream in streams:
            print(
                f"User: {stream['user_name']}, Title: {stream['title']}, Viewers: {stream['viewer_count']}")

    else:
        print("No VTuber streams found.")

if __name__ == "__main__":
    asyncio.run(main())

"""A DiscoDate discord bot."""
import sys
import os
from dotenv import load_dotenv

from interactions import Client, Intents, listen


bot = Client(intents=Intents.DEFAULT, debug_scope=True)
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


@listen()
async def on_ready():
    """Listen for being ready."""
    print("Bot is ready!")


@listen()
async def on_message_create(event):
    """Listen for messages being sent."""
    print(f"message received: {event.message.content}")


def main() -> int:
    """Do main things."""
    bot.start(TOKEN)
    return 0


if __name__ == '__main__':
    sys.exit(main())

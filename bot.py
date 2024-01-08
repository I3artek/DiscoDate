"""A DiscoDate discord bot."""
import sys
import interactions


bot = interactions.Client()


@interactions.listen()
async def on_startup():
    """Start I guess."""
    print("Bot is ready!")


def main() -> int:
    """Do main things."""
    return 0


if __name__ == '__main__':
    sys.exit(main())

"""A DiscoDate discord bot."""
import sys
import os
from dotenv import load_dotenv
from datetime import datetime

from interactions import Client, Intents, listen, slash_command, SlashContext
from interactions import slash_option, OptionType, SlashCommandChoice
from interactions import Converter, BaseContext, Task, DateTrigger, Member

load_dotenv()

SERVER_ID = os.getenv("SERVER_ID")

bot = Client(intents=Intents.DEFAULT, debug_scope=SERVER_ID)

TOKEN = os.getenv("DISCORD_TOKEN")


class Event:
    """Representation of an event."""

    invitees = []

    def __init__(self,
                 ctx: SlashContext,
                 day,
                 month,
                 year,
                 hour,
                 minute,
                 name):
        """Create event object."""
        self.ctx = ctx
        self.day = day
        self.month = month
        self.year = year
        self.hour = hour
        self.minute = minute
        self.name = name

    def date_string(self):
        """Return datestring."""
        return datetime(EVENT.year, EVENT.month,
                        EVENT.day, EVENT.hour, EVENT.minute)


EVENT: Event = None


def create_notification_callback(member, msg):
    """Create a notification that will be sent in the future."""
    async def notify_user():
        print(msg)
        await member.send(msg)
    return notify_user


@slash_command(name="set_notification",
               description="Set a notification for X hours Y minutes bofore the event")
@slash_option(
    name="hours",
    description="Hours before the event",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=0,
    max_value=23
)
@slash_option(
    name="minutes",
    description="Minutes before the event",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=0,
    max_value=59
)
@slash_option(
    name="msg",
    description="Notification message",
    required=False,
    opt_type=OptionType.STRING)
async def set_notification_handler(ctx: SlashContext,
                                   hours,
                                   minutes,
                                   msg=""):
    """Set a nofication."""
    new = datetime(EVENT.year, EVENT.month,
                   EVENT.day, EVENT.hour - hours, EVENT.minute - minutes)
    print(new)
    if msg == "":
        msg = f"{EVENT.name} starts in {hours} hours and {minutes} minutes!"
    Task(create_notification_callback(ctx.author, msg), DateTrigger(new)).start()
    await ctx.send(f"Notification set for {hours} hours and {minutes} minutes before {EVENT.name}!")


@listen()
async def on_ready():
    """Listen for being ready."""
    print("Bot is ready!")


@slash_command(name="invite_member", description="Invite someone to the event")
@slash_option(name="member",
              description="The invitee",
              opt_type=OptionType.USER,
              required=True
              )
async def invite_member_handler(ctx: SlashContext, member: Member):
    """Invite a member to an event."""
    await member.send(f"Hi! You have been invited to {EVENT.name} on {ctx.guild.name}!")
    await ctx.send(f"User {member.mention} invited to {EVENT.name}")
    pass


@slash_command(name="create_event", description="Create an event")
@slash_option(
    name="day",
    description="Day",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=1,
    max_value=31
)
@slash_option(
    name="month",
    description="Month",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=1,
    max_value=12
)
@slash_option(
    name="year",
    description="Year",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=[
        SlashCommandChoice(name="This year", value=datetime.now().year),
        SlashCommandChoice(name="Next year", value=datetime.now().year + 1)
    ]
)
@slash_option(
    name="hour",
    description="Hour",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=0,
    max_value=23
)
@slash_option(
    name="minute",
    description="Minute",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=0,
    max_value=59
)
@slash_option(
    name="name",
    description="Name of the event",
    required=True,
    opt_type=OptionType.STRING
)
async def create_event_handler(ctx: SlashContext,
                               day,
                               month,
                               year,
                               hour,
                               minute,
                               name):
    """Create an event."""
    global EVENT
    EVENT = Event(ctx, day, month, year, hour, minute, name)
    await ctx.send(f"Event {name} created! It will take place on {EVENT.date_string()}")
    pass


def main() -> int:
    """Do main things."""
    bot.start(TOKEN)
    return 0


if __name__ == '__main__':
    sys.exit(main())

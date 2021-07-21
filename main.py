from discord.ext import commands
from libs.config import config

bot = commands.Bot(command_prefix="c!")

default_cogs = ["cogsmgmt", "basic", "rooms"]


@bot.event
async def on_ready():
    print("Logged in as {} ({})".format(bot.user.name, bot.user.id))


def main():
    print(config)

    for cog in default_cogs:
        bot.load_extension(f"cogs.{cog}")

    bot.run(config.api.token)


if __name__ == "__main__":
    main()

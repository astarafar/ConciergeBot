from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):

        await ctx.channel.send(
            "API response time: `{} ms`".format(
                int(self.bot.latency * 1000)
            )
        )

    @commands.command()
    async def nsfw(self, ctx):
        exempt_channels = ["club-entrance", "rules"]
        for channel in ctx.guild.channels:
            if channel.name not in exempt_channels:
                await channel.edit(nsfw=True)


def setup(bot):
    bot.add_cog(BasicCommands(bot))

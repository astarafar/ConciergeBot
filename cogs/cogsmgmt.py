from discord.ext import commands


class CogManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cogreload(self, ctx):
        cog_name = ctx.message.content.split(" ")[1]

        print(f"Reloading cog {cog_name}...")
        await ctx.channel.send(f"Reloading cog {cog_name}...")

        self.bot.reload_extension(f"cogs.{cog_name}")

        print("Done.")
        await ctx.channel.send("Done.")

    @commands.command()
    async def cogload(self, ctx):
        cog_name = ctx.message.content.split(" ")[1]

        print(f"Loading cog {cog_name}...")
        await ctx.channel.send(f"Loading cog {cog_name}...")

        self.bot.load_extension(f"cogs.{cog_name}")

        print("Done.")
        await ctx.channel.send("Done.")

    @commands.command()
    async def cogunload(self, ctx):
        cog_name = ctx.message.content.split(" ")[1]

        print(f"Unloading cog {cog_name}...")
        await ctx.channel.send(f"Unloading cog {cog_name}...")

        self.bot.unload_extension(f"cogs.{cog_name}")

        print("Done.")
        await ctx.channel.send("Done.")


def setup(bot):
    bot.add_cog(CogManagement(bot))

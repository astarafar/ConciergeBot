import discord
from datetime import datetime
from discord import PermissionOverwrite
from discord.ext import commands, tasks
from libs.config import config
import secrets

PERMS = {
    "view_channel": True,
    "add_reactions": True,
    "send_messages": True,
    "embed_links": True,
    "attach_files": True,
    "read_message_history": True,
}

CREATOR_PERMS = {
    "view_channel": True,
    "add_reactions": True,
    "send_messages": True,
    "embed_links": True,
    "attach_files": True,
    "read_message_history": True,
    "manage_messages": True,
}


class RoomsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reap_idle_rooms.start()

    @commands.command()
    async def create(self, ctx, *args: discord.Member):
        category = ctx.guild.get_channel(
            config.private_rooms.category_id
        )

        await ctx.message.delete()

        chan_name = "room-{}".format(secrets.token_hex(2))

        overwrites = {
            user: PermissionOverwrite(**PERMS) for user in args
        }
        overwrites[ctx.author] = PermissionOverwrite(**CREATOR_PERMS)
        overwrites[ctx.guild.default_role] = PermissionOverwrite(
            view_channel=False
        )

        channel = await category.create_text_channel(
            chan_name, overwrites=overwrites, nsfw=True
        )

        mention_list = [user.mention for user in args]

        await channel.send(
            "{} - Your room is ready.".format(", ".join(mention_list))
        )

    @commands.command()
    async def delete(self, ctx):
        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.send("Only the room creator can delete the room.")
        else:
            await ctx.channel.delete()

    @tasks.loop(minutes=1)
    async def reap_idle_rooms(self):
        category = self.bot.get_channel(
            config.private_rooms.category_id
        )
        for channel in category.channels:
            if channel.name != "front-desk":
                if channel.last_message_id:
                    msg = await channel.fetch_message(
                        channel.last_message_id
                    )
                    if (
                        datetime.utcnow() - msg.created_at
                    ).total_seconds() > 86400:
                        await channel.delete()
                else:
                    if (
                        datetime.utcnow() - channel.created_at
                    ).total_seconds() > 3600:
                        await channel.delete()

    @reap_idle_rooms.before_loop
    async def before_reap_loop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(RoomsCommands(bot))

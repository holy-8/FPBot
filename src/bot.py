import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandError, CommandNotFound

import cmds


class Bot(commands.Bot):
    def __init__(self) -> None:
        super(Bot, self).__init__(
            command_prefix="!",
            intents=discord.Intents.default()
        )

    async def on_ready(self) -> None:
        await self.add_cog(
            cmds.Commands(self)
        )
        await self.tree.sync()
        print("Bot is ready! OwO.")

    async def on_command_error(self, ctx: commands.Context, error: CommandError) -> None:
        if not isinstance(error, CommandNotFound):
            raise error

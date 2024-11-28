import discord
from discord.ext import commands

import cmds
import msgs


class Bot(commands.Bot):
    def __init__(self) -> None:
        super(Bot, self).__init__(
            command_prefix="/",
            intents=discord.Intents.default()
        )

    async def on_ready(self) -> None:
        await self.add_cog(
            cmds.Commands(self)
        )
        await self.tree.sync()
        print(msgs.BOT_READY)

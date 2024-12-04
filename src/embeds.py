from discord import Embed, Colour
from discord.ext import commands

import cfg


async def message(msg: str) -> Embed:
    e = Embed(colour=Colour.pink())
    e.add_field(name=msg, value="", inline=False)
    return e


async def leaderboard(bot: commands.Bot, ldb: list[tuple[int, int]], page: int, last_page: int) -> Embed:
    e = Embed(title="Leaderboard", colour=Colour.pink())
    e.set_footer(text=f"Page {page} of {last_page}")
    for place, data in enumerate(ldb, (page - 1) * cfg.PAGE_SIZE + 1):
        id, points = data
        user = await bot.fetch_user(id)
        e.add_field(name=f"{place}. `@{user.name}`: {points:.2f}", value="", inline=False)
    return e

import math
import discord
from discord import app_commands
from discord.ext import commands

import cfg
import dbman
import embeds
import msgs


class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db = dbman.Database()

    @app_commands.allowed_installs(users=True)
    @app_commands.allowed_contexts(guilds=True, private_channels=True, dms=True)
    @app_commands.command(
        name="add_points",
        description="Changes user's balance by a provided amount.",
    )
    @app_commands.describe(
        user="Discord user whose balance will be changed.",
        points="Amount of femboy points. Can be negative.",
    )
    async def add_points(self, interaction: discord.Interaction, user: discord.User, points: float) -> None:
        if interaction.user.id not in cfg.ADMIN_LIST:
            await interaction.response.send_message(
                embed=await embeds.message(msgs.NOT_ALLOWED),
                ephemeral=True,
            )
            return
        self.db.update_user(user.id, points)
        new_bal = self.db.fetch_points(user.id)
        await interaction.response.send_message(
            embed=await embeds.message(msgs.PTS_UPDATE.format(user.name, points, new_bal)),
        )

    @app_commands.allowed_installs(users=True)
    @app_commands.allowed_contexts(guilds=True, private_channels=True, dms=True)
    @app_commands.command(
        name="my_points",
        description="View amount of your points.",
    )
    async def my_points(self, interaction: discord.Interaction) -> None:
        bal = self.db.fetch_points(interaction.user.id)
        await interaction.response.send_message(
            embed=await embeds.message(msgs.MY_BAL.format(bal)),
            ephemeral=True,
        )

    @app_commands.allowed_installs(users=True)
    @app_commands.allowed_contexts(guilds=True, private_channels=True, dms=True)
    @app_commands.command(
        name="view_points",
        description="View amount of femboy points of a specified user.",
    )
    @app_commands.describe(
        user="Discord user whose balance will be shown.",
    )
    async def view_points(self, interaction: discord.Interaction, user: discord.User) -> None:
        bal = self.db.fetch_points(user.id)
        await interaction.response.send_message(
            embed=await embeds.message(msgs.USER_BAL.format(user.name, bal)),
        )

    @app_commands.allowed_installs(users=True)
    @app_commands.allowed_contexts(guilds=True, private_channels=True, dms=True)
    @app_commands.command(
        name="leaderboard",
        description="View current femboy points leaderboard.",
    )
    @app_commands.describe(
        page=f"Page number, must be greater than 0. Each page shows {cfg.PAGE_SIZE} results.",
    )
    async def leaderboard(self, interaction: discord.Interaction, page: int = 1) -> None:
        try:
            leaderboard = self.db.leaderboard(page, cfg.PAGE_SIZE)
        except ValueError:
            await interaction.response.send_message(
                embed=await embeds.message("Error! Page number must be greater than 0."),
                ephemeral=True,
            )
            return
        last_page = math.ceil(self.db.count_users() / cfg.PAGE_SIZE)
        if page > (last_page):
            await interaction.response.send_message(
                embed=await embeds.message(f"Error! Page number out of range. Last available page is {last_page}."),
                ephemeral=True,
            )
            return
        if not leaderboard:
            await interaction.response.send_message(
                embed=await embeds.message("Error! Leaderboard has nothing to show."),
                ephemeral=True,
            )
            return
        await interaction.response.send_message(
            embed=await embeds.leaderboard(self.bot, leaderboard, page, last_page),
        )

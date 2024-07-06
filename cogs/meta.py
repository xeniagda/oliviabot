import discord
from discord.ext import commands
import git

from bot import OliviaBot, Context


class Meta(commands.Cog):
    """Commands related to the behavior of the bot itself"""

    @commands.command()
    async def hello(self, ctx: Context):
        """Hi!"""
        await ctx.send(f"Hello! I'm {ctx.me}!")

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def nick(self, ctx: Context):
        automated = [
            "\N{COMBINING LATIN SMALL LETTER A}",
            "\N{COMBINING LATIN SMALL LETTER U}",
            "\N{COMBINING LATIN SMALL LETTER T}",
            "\N{COMBINING LATIN SMALL LETTER O}",
            "\N{COMBINING LATIN SMALL LETTER M}",
            "\N{COMBINING LATIN SMALL LETTER A}",
            "\N{COMBINING LATIN SMALL LETTER T}",
            "\N{COMBINING LATIN SMALL LETTER E}",
            "\N{COMBINING LATIN SMALL LETTER D}",
        ]

        assert isinstance(ctx.author, discord.Member)
        assert isinstance(ctx.me, discord.Member)
        name = ctx.author.display_name
        if len(name) >= 9:
            nick = name[:-9] + "".join(a + b for a, b in zip(name[-9:], automated))
        elif len(name) >= 4:
            nick = name[:-4] + "".join(a + b for a, b in zip(name[-4:], automated[:4]))
        else:
            return await ctx.send("Nickname too short")

        await ctx.me.edit(nick=nick)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: Context):
        for extension in self.bot.activated_extensions:
            await self.bot.reload_extension(extension)
        await ctx.send("Loaded all extensions")

    @commands.command()
    async def about(self, ctx: Context):
        """About me!"""
        lines = []
        for commit in self.repo.iter_commits(max_count=5):
            url = f"[`{commit.hexsha[:7]}`](https://RocketRace/oliviabot/commit/{commit.hexsha})"
            dt = discord.utils.format_dt(commit.committed_datetime, "R")
            full_summary = (
                bytes(commit.summary).decode("utf-8")
                if not isinstance(commit.summary, str)
                else commit.summary
            )
            summary = (
                full_summary[:17] + "..." if len(full_summary) > 20 else full_summary
            )
            changes = f"+{commit.stats.total["insertions"]} -{commit.stats.total["deletions"]}"
            lines.append(f"{url} {dt} {changes} {summary}")
        embed = discord.Embed(
            description="Hi! I'm oliviabot, an automated version of Olivia."
                        "I try my best to provide joy to the world."
        )
        embed.add_field(name="Recent commits", value="".join(lines), inline=False)
        await ctx.send(embed=embed)

    def __init__(self, bot: OliviaBot):
        self.repo = git.Repo(".")
        self.bot = bot


async def setup(bot: OliviaBot):
    await bot.add_cog(Meta(bot))

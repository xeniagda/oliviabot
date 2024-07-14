from discord.ext import commands, tasks

from bot import OliviaBot


class Reloader(commands.Cog):
    """Automatic bot reloading, to replace the Terminal cog in prod"""

    def __init__(self, bot: OliviaBot):
        self.is_reloading = False
        self.bot = bot
        self.check_for_extensions.start()

    async def cog_unload(self):
        self.check_for_extensions.cancel()

    @tasks.loop(seconds=5.0)
    async def check_for_extensions(self):
        changes = [change.strip().split(":") for change in open(".extensions")]
        if changes:
            for action, extension in changes:
                match action:
                    case "load":
                        await self.bot.load_extension(extension)
                    case "unload":
                        await self.bot.unload_extension(extension)
                    case "reload":
                        await self.bot.reload_extension(extension)
            open(".extensions").truncate(0)
            results = ", ".join(
                f"{action}ed `{extension}`" for action, extension in changes
            )
            await self.bot.webhook.send(f"Updated extensions: {results}")


async def setup(bot: OliviaBot):
    await bot.add_cog(Reloader(bot))

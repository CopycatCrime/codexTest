import traceback
import discord
from discord.ext import commands
from config import BotConfig

intent = discord.Intents.all()


class DiscordBot(commands.Bot):
    def __init__(self, **kwargs):
        intents = discord.Intents.all()
        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents, **kwargs, pm_help=None,
                         help_attrs=dict(hidden=True))

    async def setup_hook(self) -> None:
        for extension in BotConfig.cogs:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print('Could not load extension {0} due to {1.__class__.__name__}: {1}'.format(
                    extension, e))
        await self.tree.sync()

    async def on_ready(self):
        print('Logged on as {0} (ID: {0.id})'.format(self.user))

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return

        orig_error = getattr(error, "original", error)
        error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
        error_msg = "```py\n" + error_msg + "\n```"
        await ctx.send(error_msg)


bot = DiscordBot()
bot.run(BotConfig.token)

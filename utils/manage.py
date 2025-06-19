from discord.ext import commands
import discord

class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.members = []

    @commands.command()
    async def add_member(self, ctx, member: discord.Member):
        self.members.append(member)
        await ctx.send(f"{member.name}を追加しました")

    @commands.command()
    async def remove_member(self, ctx, member: discord.Member):
        self.members.remove(member)
        await ctx.send(f"{member.name}を削除しました")

    
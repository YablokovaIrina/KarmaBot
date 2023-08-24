import disnake
import os
from disnake.ext import commands

from utils import database

from dotenv import load_dotenv


load_dotenv()


CENSORED_WORDS = ['карма', 'карму', 'кармы', 'карме']


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = database.DataBase()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.db.create_table()

        for guild in self.bot.guilds:
            for member in guild.members:
                role = disnake.utils.get(guild.roles, id=int(os.getenv("UR")))
                if role in member.roles:
                    await self.db.insert_new_member(member)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.db.insert_new_member(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.db.delete_member(member)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.process_commands(message)

        for content in message.content.split():
            for censored_word in CENSORED_WORDS:
                if content.lower() == censored_word and message.author != self.bot.user:
                    await message.channel.send(f"{message.author.mention} будет карма, будет...")


def setup(bot):
    bot.add_cog(Events(bot))

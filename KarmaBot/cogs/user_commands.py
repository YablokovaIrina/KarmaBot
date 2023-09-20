import os
import disnake
from disnake.ext import commands

from utils import database
from utils.pagination import PaginatorView, AuthorView

from dotenv import load_dotenv


load_dotenv()


class UserCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = database.DataBase()

    @commands.slash_command(
        description="Бот ты тут?"
    )
    async def test(self, ctx):
        await ctx.send('Опять всю карму засрали...')

    @commands.slash_command(
        description="Все команды"
    )
    async def info(self, ctx):
        await ctx.send(f'{ctx.author.mention}\n'
                       f'/test - Бот ты тут?\n'
                       f'/karma - Твоя карма\n'
                       f'/karma_list - Карма всех участников\n'
                       f'/add_karma - Добавление кармы участнику (Доступно только для офицеров)\n'
                       f'/delete_karma - Убавление или удаление кармы участнику (Доступно только для офицеров)\n')

    @commands.slash_command(
        description="Твоя карма/карма другого участника"
    )
    async def karma(self, ctx, member: disnake.Member = None):
        karma = await self.db.get_user(ctx.author)
        embed = disnake.Embed(description=f"**Карма {ctx.author.display_name}: {karma[2]}**")

        if member is not None:
            karma = await self.db.get_user(member)
            embed.description = f"**Карма {member.display_name}: {karma[2]}**"
        await ctx.send(embed=embed)

    @commands.slash_command(
        description="Добавление кармы"
    )
    @commands.has_role(int(os.getenv('ADMIN')))
    async def add_karma(self, ctx, member: disnake.Member = None, amount: int = None):
        if member is None:
            await ctx.send(f"{ctx.author.display_name}, укажите участника")
        else:
            if amount is None:
                await ctx.send(f"{ctx.author.display_name}, укажите количество очков кармы")
            elif amount < 1:
                await ctx.send(f"{ctx.author.display_name}, укажите более 1")
            else:
                await self.db.update_member("UPDATE users SET karma = karma + ? WHERE id = ?", [amount, member.id])
                karma = await self.db.get_user(member)
                await ctx.send(f"Карма {member.display_name} была успешно добавлена!\n" \
                               f"""**Карма {member.display_name}**: {karma[2]}""")

    @commands.slash_command(
        description="Убавление или удаление кармы"
    )
    @commands.has_role(int(os.getenv('ADMIN')))
    async def delete_karma(self, ctx, member: disnake.Member, amount: int = None):
        if member is None:
            await ctx.send(f"{ctx.author.display_name}, укажите участника")
        else:
            if amount is None:
                await ctx.send(f"{ctx.author.display_name}, укажите количество очков кармы")
            elif amount == 000:
                await self.db.update_member("UPDATE users SET karma = ? WHERE id = ?",
                                            [0, member.id])
                karma = await self.db.get_user(member)
                await ctx.send(f"Карма {member.display_name} была успешно удалена!\n" \
                               f"""**Карма {member.display_name}**: {karma[2]}""")
            elif amount < 1:
                await ctx.send(f"{ctx.author.display_name}, укажите более 1")
            else:
                await self.db.update_member("UPDATE users SET karma = karma - ? WHERE id = ?",
                                            [amount, member.id])
                karma = await self.db.get_user(member)
                await ctx.send(f"Карма {member.display_name} была успешно удалена!\n" \
                               f"""**Карма {member.display_name}**: {karma[2]}""")

    @commands.slash_command(
        description="Карма всех участников"
    )
    async def karma_list(self, ctx):
        counter = 0
        data = await self.db.get_data()
        embeds = []
        n = 0
        text = ''

        for row in data:
            counter += 1
            n += 1
            text += (f'**#{counter} | {row["name"]}** \n'
                     f'Карма: {row["karma"]} \n'
                     f'\n')
            if n % 10 == 0 or n - 1 == len(data) - 1:
                embed = disnake.Embed(color=0x2F3136, title='Карма NP UR')
                embed.description = text
                embeds.append(embed)
                text = ''

        class ServerPagesView(AuthorView, PaginatorView):
            pass

        view = ServerPagesView(ctx.author, embeds=embeds)
        await ctx.send(embed=embeds[0], view=view)


def setup(bot):
    bot.add_cog(UserCommands(bot))

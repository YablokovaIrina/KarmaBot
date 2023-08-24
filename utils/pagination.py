import disnake
from disnake import ButtonStyle


class AuthorView(disnake.ui.View):
    """A view with an interaction check allowing only
    the command author to interact with the view"""

    def __init__(self, author: disnake.User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author

    async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
        if inter.author != self.author:
            embed = disnake.Embed(
                title="This isn't your command!",
                description="You cannot interact with a command you did not call.",
                color=disnake.Color.red(),
            )
            await inter.send(ephemeral=True, embed=embed)
            return False
        return await super(AuthorView, self).interaction_check(inter)


class PaginatorView(disnake.ui.View):
    """Defines a simple paginator of buttons for the embed."""

    def __init__(self, embeds: list[disnake.Embed]):
        super().__init__(timeout=300)
        self.embeds = embeds
        self.change_page(0)
        self.embed_count = 0

        self.first_page.disabled = True
        self.prev_page.disabled = True
        # no buttons if there is only one page
        if len(embeds) <= 1:
            self.children = []

    @disnake.ui.button(emoji="<:arrowfirst:955585658615910451>", style=ButtonStyle.gray)
    async def first_page(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        self.change_page(0)
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = True
        self.prev_page.disabled = True
        self.next_page.disabled = False
        self.last_page.disabled = False
        await inter.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="<:arrowleft:955585658922102844>", style=ButtonStyle.gray)
    async def prev_page(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        self.change_page(self.embed_count - 1)
        embed = self.embeds[self.embed_count]

        self.next_page.disabled = False
        self.last_page.disabled = False
        if self.embed_count == 0:
            self.first_page.disabled = True
            self.prev_page.disabled = True
        await inter.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(style=ButtonStyle.blurple, label="...")
    async def page(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()

    @disnake.ui.button(emoji="<:arrowright:955585658863357972>", style=ButtonStyle.gray)
    async def next_page(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        self.change_page(self.embed_count + 1)
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        if self.embed_count == len(self.embeds) - 1:
            self.next_page.disabled = True
            self.last_page.disabled = True
        await inter.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="<:arrowlast:955585658867572787>", style=ButtonStyle.gray)
    async def last_page(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        self.change_page(len(self.embeds) - 1)

        embed = self.embeds[self.embed_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        self.next_page.disabled = True
        self.last_page.disabled = True
        await inter.response.edit_message(embed=embed)

    def change_page(self, new_index):
        self.embed_count = new_index
        self.page.label = f"{self.embed_count+1}/{len(self.embeds)}"

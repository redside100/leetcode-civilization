import time
import discord

from consts import BATTLE_TIMEOUT
import db
import lcapi
from util import create_embed


class BattleCancelRequest(discord.ui.View):
    def __init__(self, id_a: int, id_b: int, battle_cache, battle_cancel_cache):
        self.id_a = id_a
        self.id_b = id_b
        self.battle_cache = battle_cache
        self.battle_cancel_cache = battle_cancel_cache
        super().__init__(timeout=60)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.id_b:
            return False
        return True

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, _):

        if self.id_a in self.battle_cache:
            del self.battle_cache[self.id_a]

        if self.id_b in self.battle_cache:
            del self.battle_cache[self.id_b]

        if (self.id_a, self.id_b) in self.battle_cancel_cache:
            del self.battle_cancel_cache[(self.id_a, self.id_b)]

        await interaction.response.send_message(
            f"<@{self.id_a}> <@{self.id_b}>",
            embed=create_embed("Leetcode battle cancelled!"),
        )

        self.stop()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, _):

        if (self.id_a, self.id_b) in self.battle_cancel_cache:
            del self.battle_cancel_cache[(self.id_a, self.id_b)]

        await interaction.response.send_message(
            embed=create_embed(
                f"<@{self.id_b}> declined the cancel request.",
            )
        )

        self.stop()


class BattleRequest(discord.ui.View):
    def __init__(
        self,
        id_a: int,
        id_b: int,
        a_info: dict,
        b_info: dict,
        request_cache,
        battle_cache,
        difficulty: str,
    ):
        self.id_a = id_a
        self.id_b = id_b
        self.a_info = a_info
        self.b_info = b_info
        self.request_cache = request_cache
        self.battle_cache = battle_cache
        self.difficulty = difficulty
        super().__init__(timeout=120)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.id_b:
            return False
        return True

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, _):
        if (self.id_a, self.id_b) in self.request_cache:
            del self.request_cache[(self.id_a, self.id_b)]

        if self.id_a in self.battle_cache or self.id_b in self.battle_cache:
            await interaction.response.send_message(embed=create_embed("One or more users are already in a battle."))
            self.stop()
            return
        
        await interaction.response.defer(thinking=True)
        problem = await lcapi.get_random_problem(difficulty=self.difficulty.upper())

        has_noob = self.a_info["rank"] == "Noob" or self.b_info["rank"] == "Noob"

        self.battle_cache[self.id_a] = (
            self.id_b,
            problem["titleSlug"],
            problem["difficulty"],
            has_noob,
        )
        self.battle_cache[self.id_b] = (
            self.id_a,
            problem["titleSlug"],
            problem["difficulty"],
            has_noob,
        )
        exp_time = int(time.time() + BATTLE_TIMEOUT)
        await interaction.followup.send(
            f"<@{self.id_a}> <@{self.id_b}>",
            embed=create_embed(
                title="Leetcode Battle",
                message=f"The battle problem is **[{problem["title"]}](https://leetcode.com/problems/{problem["titleSlug"]})**."
                + f"\nThe first one to submit an accepted answer and uses `/submit` wins!\nThis battle expires <t:{exp_time}:R>.",
            ),
        )

        self.stop()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, _):

        await interaction.response.send_message(
            embed=create_embed(
                f"<@{self.id_b}> declined the battle request.",
            )
        )

        if (self.id_a, self.id_b) in self.request_cache:
            del self.request_cache[(self.id_a, self.id_b)]

        self.stop()

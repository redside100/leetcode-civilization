import functools
import random
from typing import Optional
from cachetools import TTLCache
import discord

from consts import RANK_VALUE, RANKDOWN_PROGRESSION, RANKUP_PROGRESSION
import db
import lcapi


def create_embed(message: str, title: Optional[str] = None):
    embed = discord.Embed(color=0xFFAE00)
    embed.description = message
    if title:
        embed.title = title
    return embed


def create_profile_embed(info: dict, lc_info: dict, title: str, avatar):
    embed = discord.Embed(color=0xFFAE00)
    embed.title = title

    if not avatar:
        url = "https://cdn.discordapp.com/embed/avatars/0.png"
    else:
        url = avatar.url

    embed.set_thumbnail(url=url)

    embed.add_field(name="LC User", value=info["leetcode_handle"])
    if info["rank"] == "Champion":
        embed.add_field(name="Rank", value=f"{info['rank']} ({info['champion_lp']} LP)")
    else:
        embed.add_field(name="Rank", value=info["rank"])

    embed.add_field(name="Tickets", value=info["tickets"])

    embed.add_field(name="Easies", value=lc_info["EASY"])
    embed.add_field(name="Mediums", value=lc_info["MEDIUM"])
    embed.add_field(name="Hards", value=lc_info["HARD"])

    embed.add_field(name="Wins", value=info["wins"])
    embed.add_field(name="Losses", value=info["losses"])
    embed.set_footer(
        text="Number of solved questions are not realtime - sync with /sync"
    )

    return embed


def user_command(fetch_lc=False):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(interaction: discord.Interaction, *args, **kwargs):
            user_data = await db.get_info(interaction.user.id)

            async def noop(interaction: discord.Interaction, *args, **kwargs):
                await interaction.response.send_message(
                    embed=create_embed("You don't have an account linked!"),
                    ephemeral=True,
                )

            if not user_data:
                return await noop(interaction, *args, **kwargs)

            if fetch_lc:
                lc_info = await lcapi.get_solve_count(user_data["leetcode_handle"])
            else:
                lc_info = None

            interaction.data["injected"] = (user_data, lc_info)

            return await func(interaction, *args, **kwargs)

        return wrapped

    return wrapper


def has_active_battle_request(cache: TTLCache, id_a: int, id_b: int):
    key = (id_a, id_b)
    rev_key = (id_b, id_a)

    return key in cache or rev_key in cache


def get_lp_delta(user_info: dict, opponent_info: dict, problem_difficulty: str):
    # LP calcs
    base_lp = {
        "Easy": 8,
        "Medium": 12,
        "Hard": 20,
    }
    lp_diff = opponent_info["champion_lp"] - user_info["champion_lp"]
    if lp_diff < 0:
        lp_delta = base_lp[problem_difficulty] + random.randint(0, 3)
    else:
        lp_delta = (
            base_lp[problem_difficulty]
            + random.randint(0, 3)
            + int(min(lp_diff / 10, 10))
        )
    return lp_delta


async def handle_battle_result(
    user_info: dict,
    opponent_info: dict,
    problem_difficulty: str,
    user_id: int,
    opponent_id: int,
):
    result_msg = ""
    lp_delta = get_lp_delta(user_info, opponent_info, problem_difficulty)

    await db.set_wins(user_id, user_info["wins"] + 1)
    await db.set_losses(opponent_id, opponent_info["losses"] + 1)

    if opponent_info["rank"] == "Noob" or user_info["rank"] == "Noob":
        result_msg = "Nothing happens because someone is a Noob."
    else:
        # handle opponent losses
        if opponent_info["rank"] == "Champion":
            result_msg += f"<@{opponent_id}> lost **{lp_delta}** LP.\n"
            if opponent_info["champion_lp"] - lp_delta < 0:
                await db.set_lp(opponent_id, 0)
                await db.set_rank(opponent_id, "Master")
                result_msg += f"<@{opponent_id}>'s LP fell below 0, so they are now a Leetcode **Master**.\n"
            else:
                await db.set_lp(opponent_id, opponent_info["champion_lp"] - lp_delta)
        else:
            # rank loss
            await db.set_rank(opponent_id, RANKDOWN_PROGRESSION[opponent_info["rank"]])
            result_msg += f"<@{opponent_id}> is now a Leetcode **{RANKDOWN_PROGRESSION[opponent_info["rank"]]}**.\n"

        # handle user gains
        if user_info["rank"] == "Champion" and opponent_info["rank"] == "Champion":
            lp_delta = get_lp_delta(user_info, opponent_info, problem_difficulty)

            result_msg += f"<@{user_id}> gained **{lp_delta}** LP.\n"
            await db.set_lp(user_id, user_info["champion_lp"] + lp_delta)
        else:
            rank_polarity = (
                RANK_VALUE[user_info["rank"]] - RANK_VALUE[opponent_info["rank"]]
            )
            # lower rank than opponent
            if rank_polarity < 0:
                await db.set_rank(
                    user_id,
                    RANKUP_PROGRESSION[user_info["rank"]]["next_rank"],
                )
                result_msg += f"<@{user_id}> is now a Leetcode **{RANKUP_PROGRESSION[user_info["rank"]]["next_rank"]}**."
            else:
                # same rank or higher
                base_difficulty_tickets = {
                    "Easy": 10,
                    "Medium": 20,
                    "Hard": 35,
                }
                await db.set_tickets(
                    user_id,
                    user_info["tickets"] + base_difficulty_tickets[problem_difficulty],
                )
                result_msg += f"<@{user_id}> gains **{base_difficulty_tickets[problem_difficulty]}** tickets."

    return result_msg


def wrap_lc_info(user_info: dict):
    return {
        "EASY": user_info["easies"],
        "MEDIUM": user_info["mediums"],
        "HARD": user_info["hards"],
    }

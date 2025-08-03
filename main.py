import os
import discord
import json
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ✅ Add your Domme role IDs to this list
# ❗ You MUST replace the placeholder IDs with your actual role IDs
DOMME_ROLE_IDS = [
    1399961473291128934,  # Domme Role 1
    1399992393897349193 ,  # Domme Role 2
    1399992161243627520,  # Domme Role 3
    3333333333333333333,  # Domme Role 4
]

CURRENCY_NAME = "ObediencePoint"
CURRENCY_SYMBOL = "<:pawcoin:1400486081727697077>"

POINTS_FILE = "points.json"

# Load points from JSON file
def load_points():
    if os.path.exists(POINTS_FILE):
        with open(POINTS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save points to JSON file
def save_points():
    with open(POINTS_FILE, "w") as f:
        json.dump(points, f)

points = load_points()

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {bot.user}")

# ✅ Updated function to check for multiple Domme roles
def has_domme_role(interaction: discord.Interaction) -> bool:
    user_role_ids = [role.id for role in interaction.user.roles]
    return any(role_id in DOMME_ROLE_IDS for role_id in user_role_ids)

@tree.command(name="givepoints", description="Give obedience points to a user")
@app_commands.describe(user="User to give points to", amount="Amount of points to give")
async def givepoints(interaction: discord.Interaction, user: discord.Member, amount: int):
    if not has_domme_role(interaction):
        await interaction.response.send_message("⛔ You don't have permission to give points.", ephemeral=True)
        return

    user_id = str(user.id)
    points[user_id] = points.get(user_id, 0) + amount
    save_points()
    await interaction.response.send_message(
        f"{amount} {CURRENCY_NAME}(s) {CURRENCY_SYMBOL} have been awarded to {user.mention}."
    )

@tree.command(name="removepoints", description="Remove obedience points from a user")
@app_commands.describe(user="User to remove points from", amount="Amount of points to remove")
async def removepoints(interaction: discord.Interaction, user: discord.Member, amount: int):
    if not has_domme_role(interaction):
        await interaction.response.send_message("⛔ You don't have permission to remove points.", ephemeral=True)
        return

    user_id = str(user.id)
    points[user_id] = max(0, points.get(user_id, 0) - amount)
    save_points()
    await interaction.response.send_message(
        f"{amount} {CURRENCY_NAME}(s) {CURRENCY_SYMBOL} have been removed from {user.mention}."
    )

@tree.command(name="leaderboard", description="Show the top obedient users")
async def leaderboard(interaction: discord.Interaction):
    if not points:
        await interaction.response.send_message("No one has any Obedience Points yet.")
        return

    sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
    leaderboard_text = "\n".join(
        [f"**{i+1}.** <@{uid}> — {amt} {CURRENCY_SYMBOL}" for i, (uid, amt) in enumerate(sorted_points)]
    )
    await interaction.response.send_message(f"**🏆 Obedience Leaderboard**\n\n{leaderboard_text}")

# ✅ Secure token load from Replit secret
from keep_alive import keep_alive
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))

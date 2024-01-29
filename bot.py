import discord
from discord.ext import commands
import datetime
import random

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or(''), intents=intents, help_command=commands.DefaultHelpCommand())

# Add your application ID and public key here
application_id = 1195902422879580282
public_key = "9aa33fa40fbbd7d78eb26715d886e5dbbfcd80b4c384688f3f140268f5e17e18"

user_points = {}
coaching_levels = {}  # To track coaching levels (green, yellow, red, terminated)
coaching_history = {}
last_message_date = {}

corporate_messages = [
    "Thank you for your creative use of time. Please remember, time is money!",
    "We appreciate your dedication to diversifying our content with links. Keep up the great work!",
    "In the spirit of efficiency, let's focus on work-related messages. Thank you!",
    "Your commitment to sharing valuable links is unparalleled. Keep those links coming!",
    "Remember, time spent sharing links is time not spent working. Let's prioritize our tasks!",
    "Your dedication to multimedia communication is noted. Let's channel that energy into productivity!",
    "In the corporate world, every message counts. Let's make them all count towards our goals!",
    "We value your input, but let's redirect our efforts towards work-related discussions. Thank you!",
    "Your commitment to sharing visual content is commendable. Let's align our visuals with company goals!",
    "In the grand scheme of things, every message contributes to our success. Let's keep it focused!",
]

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.command(name='coach')
async def coach(ctx, member: discord.Member, *, reason=None):
    coach_target_id = member.id

    if coach_target_id not in coaching_levels:
        coaching_levels[coach_target_id] = 0  # Initialize coaching level to green

    if coach_target_id not in coaching_history:
        coaching_history[coach_target_id] = []

    coaching_levels[coach_target_id] += 1

    if coaching_levels[coach_target_id] >= 5:
        await ctx.send(f"{member.mention}, Terminated! 🔥")
        coaching_levels[coach_target_id] = 0
    else:
        level_names = ["Green", "Yellow", "Red", "Terminated"]
        coaching_history[coach_target_id].append({"level": coaching_levels[coach_target_id], "reason": reason})
        await ctx.send(f"{member.mention}, Coaching level: {level_names[coaching_levels[coach_target_id]]}, Reason: {reason}")

@bot.command(name='vcoach')
async def view_coachings(ctx, member: discord.Member):
    coach_target_id = member.id

    if coach_target_id in coaching_history:
        coachings = coaching_history[coach_target_id]
        if coachings:
            output = f"{member.display_name}'s Coaching History:\n"
            for coaching in coachings:
                output += f"Level {coaching['level']}: {coaching['reason']}\n"
            await ctx.send(output)
        else:
            await ctx.send(f"{member.display_name} has no coaching history.")
    else:
        await ctx.send(f"{member.display_name} has no coaching history.")

@bot.command(name='reset')
async def reset(ctx):
    user_id = ctx.author.id

    if user_id in coaching_levels:
        coaching_levels[user_id] = 0
        user_points[user_id] = 0
        await ctx.send(f"{ctx.author.mention}, You have reset your coaching level and points. You can now interact with the bot's commands again.")

@bot.command(name='addpoints')
async def add_points(ctx, member: discord.Member, points: int):
    user_id = member.id

    if user_id in user_points:
        user_points[user_id] += points
    else:
        user_points[user_id] = points

    await ctx.send(f"{member.mention}, You have been awarded {points} points. Your total points: {user_points[user_id]}")

@bot.command(name='points')
async def view_points(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    user_id = member.id

    if user_id in user_points:
        await ctx.send(f"{member.mention}, You have {user_points[user_id]} points.")
    else:
        await ctx.send(f"{member.mention}, You have 0 points.")

bot.run('MTE5NTkwMjQyMjg3OTU4MDI4Mg.GBVgJ9.aK8MVIIKNe1J7UIBvbL0VpThws7xPoA1ZVL4LQ')

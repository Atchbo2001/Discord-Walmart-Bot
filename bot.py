import discord
from discord.ext import commands, tasks
import datetime
import random

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

user_points = {}
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

@bot.command(name='coach', pass_context=True)
async def coach(ctx, member: discord.Member, *, reason=None):
    coach_author_id = ctx.author.id
    coach_target_id = member.id

    if coach_target_id not in coaching_history:
        coaching_history[coach_target_id] = []

    if coach_target_id not in user_points:
        user_points[coach_target_id] = 0

    if user_points[coach_target_id] >= 5:
        await ctx.send(f"{member.mention}, Fired! 🔥")
        user_points[coach_target_id] = 0
    else:
        user_points[coach_target_id] += 1
        coaching_history[coach_target_id].append({"level": user_points[coach_target_id], "reason": reason})
        await ctx.send(f"{member.mention}, Coach level: {user_points[coach_target_id]}, Reason: {reason}")

@bot.command(name='view_coachings', pass_context=True)
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

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id

    if user_id not in user_points:
        user_points[user_id] = 0

    if user_id not in last_message_date:
        last_message_date[user_id] = datetime.datetime.now()

    current_date = datetime.datetime.now()
    days_since_last_message = (current_date - last_message_date[user_id]).days

    user_points[user_id] += days_since_last_message
    last_message_date[user_id] = current_date

    if user_points[user_id] >= 5:
        await message.channel.send(f"{message.author.mention}, Fired! 🔥")
        user_points[user_id] = 0
    else:
        # Check for links or pictures
        if any(word in message.content.lower() for word in ['http', 'www', '.com', '.net']) or message.attachments:
            await message.channel.send(f"{message.author.mention}, {random.choice(corporate_messages)}")
        else:
            await bot.process_commands(message)

# Replace 'YOUR_BOT_TOKEN' with your actual Discord bot token
bot.run('YOUR_BOT_TOKEN')

import discord
import json
import asyncio

with open('config.json') as config_file:
  data = json.load(config_file)
  token = data['token']

bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
  print(f"Logged in as {bot.user.name}")

@bot.slash_command(name="ban", description="Bans the selected user from the server", permissions=["ban_members"])
async def ban(ctx, user: discord.User, reason: str = "No reason provided"):
  guild = ctx.guild
  await guild.ban(user, reason=reason)
  await ctx.send(f"{user.name} has been banned from the server. Reason: {reason}")

@bot.slash_command(name="kick", description="Kicks the selected user from the server", permissions=["kick_members"])
async def kick(ctx, user: discord.User, reason: str = "No reason provided"):
  guild = ctx.guild
  await guild.kick(user, reason=reason)
  await ctx.send(f"{user.name} has been kicked from the server. Reason: {reason}")

@bot.slash_command(name="reminder", description="Set a reminder and receive a reminder over direct messages")
async def reminder(ctx, duration: int, reminder_message: str):
  user = ctx.author
  await ctx.send(f"Reminder set for {duration} seconds from now.")
  await asyncio.sleep(duration)
  await user.send(f"Reminder: {reminder_message}")

@bot.slash_command(name="ping", description="Returns the bot's latency")
async def ping(ctx):
  latency = bot.latency * 1000
  await ctx.send(f"Pong! {round(latency)}ms")

@bot.slash_command(name="avatar", description="Returns the user's avatar")
async def avatar(ctx, user: discord.User):
  avatar_url = user.avatar_url
  await ctx.send(avatar_url)

@bot.slash_command(name="purge", description="Purges the selected amount of messages", permissions=["manage_messages"])
async def purge(ctx, amount: int):
  await ctx.channel.purge(limit=amount)
  await ctx.send(f"Purged {amount} messages!")

bot.run(token)

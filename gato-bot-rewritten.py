import discord
import json
import asyncio
import random

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

@bot.slash_command(name="unban", description="Unbans a user from the server", permissions=["ban_members"])
async def unban(ctx, user: discord.User):
  guild = ctx.guild
  await guild.unban(user)
  await ctx.send(f"{user.name} has been unbanned from the server.")

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

@bot.slash_command(name="serverinfo", description="Displays information about the server", permissions=["manage_guild"])
async def serverinfo(ctx):
  guild = ctx.guild
  name = guild.name
  description = guild.description
  owner = guild.owner
  id = guild.id
  region = guild.region
  member_count = guild.member_count
  icon = guild.icon_url
  embed = discord.Embed(title=name, description=description, color=discord.Color.blue())
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Member Count", value=member_count, inline=True)
  await ctx.send(embed=embed)

@bot.slash_command(name="8ball", description="Answers a yes/no question")
async def eight_ball(ctx, question: str):
  responses = ["It is certain.",
               "It is decidedly so.",
               "Without a doubt.",
               "Yes - definitely.",
               "You may rely on it.",
               "As I see it, yes.",
               "Most likely.",
               "Outlook good.",
               "Yes.",
               "Signs point to yes.",
               "Reply hazy, try again.",
               "Ask again later.",
               "Better not tell you now.",
               "Cannot predict now.",
               "Concentrate and ask again.",
               "Don't count on it.",
               "My reply is no.",
               "My sources say no.",
               "Outlook not so good.",
               "Very doubtful."]
  await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

@bot.slash_command(name="about", description="Displays information about the bot")
async def about(ctx):
  embed = discord.Embed(title="Gato Bot Rewritten", description=" A multi-function bot for Discord. Efficiency, Stability and Customizability.", color=discord.Color.green())
  embed.add_field(name="GitHub", value="[GitHub Repository](https://github.com/notxofo/gato-bot-rewritten)")
  embed.set_footer(text="Created by notxofo")
  await ctx.send(embed=embed)

bot.run(token)

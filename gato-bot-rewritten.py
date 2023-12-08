import discord
import json
import asyncio
import random
import requests
import aiohttp

with open('config.json') as config_file:
    data = json.load(config_file)
    token = data['token']

bot = discord.Bot(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print("Welcome to Gato Bot Rewritten, created by Xofo!")


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
    avatar_url = user.avatar.url
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
    embed = discord.Embed(title="Gato Bot Rewritten",
                          description="A multi-function bot for Discord. Efficient, Stable and Customizable.",
                          color=discord.Color.green())
    embed.add_field(name="GitHub", value="[GitHub Repository](https://github.com/notxofo/gato-bot-rewritten)")
    embed.set_footer(text="Contact: notxofo")
    await ctx.send(embed=embed)


@bot.slash_command(name="dog", description="Sends a random dog image")
async def dog(ctx):
    dogpicture = requests.get("https://dog.ceo/api/breeds/image/random").json().get("message", "Not found")
    await ctx.send(f"{dogpicture}")


@bot.slash_command(name="cat", description="Sends a random cat image")
async def cat(ctx):
    catpicture = requests.get("https://api.thecatapi.com/v1/images/search").json()[0].get("url", "Not found")
    await ctx.send(f"{catpicture}")


@bot.slash_command(name="userinfo", description="Displays information about the selected user")
async def userinfo(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    if user:
        embed = discord.Embed(title="User Info", color=discord.Color.blue())
        embed.add_field(name="Username", value=user.name, inline=False)
        embed.add_field(name="User ID", value=user.id, inline=False)
        embed.add_field(name="Account Creation Date", value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("https://http.cat/images/404.jpg")


@bot.slash_command(name="servericon", description="Displays the server's icon")
async def servericon(ctx):
    guild = ctx.guild
    if guild.icon:
        icon = guild.icon.url
        await ctx.send(icon)
    else:
        await ctx.send("This server does not have an icon.")


@bot.slash_command(name="serverbanner", description="Displays the server's banner")
async def serverbanner(ctx):
    guild = ctx.guild
    if guild.banner:
        banner = guild.banner.url
        await ctx.send(banner)
    else:
        await ctx.send("This server does not have a banner.")


@bot.slash_command(name="stealemoji", description="Steals an emoji via URL", permissions=["manage_emojis"])
async def stealemoji(ctx, emoji_url: str, emoji_name: str):
    if emoji_url.endswith((".png", ".jpg", ".jpeg", ".gif")):
        async with aiohttp.ClientSession() as session:
            async with session.get(emoji_url) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = await resp.read()
        await ctx.guild.create_custom_emoji(name=emoji_name, image=data)
        await ctx.send(f"Emoji {emoji_name} has been added to the server!")
    else:
        await ctx.send(
            "Error adding emoji. Please check the URL and make sure you are using the correct image format. If the "
            "error persists, please contact the bot owner.")


@bot.slash_command(name="slowmode", description="Sets the channel's slowmode", permissions=["manage_channels"])
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Slowmode set to {seconds} seconds!")


@bot.slash_command(name="poll", description="Creates a poll", permissions=["manage_messages"])
async def poll(ctx, question: str, option1: str, option2: str):
    embed = discord.Embed(title=question, color=discord.Color.blue())
    embed.add_field(name="Option 1", value=option1, inline=False)
    embed.add_field(name="Option 2", value=option2, inline=False)
    message = await ctx.send(embed=embed)
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")

@bot.slash_command(name="help", description="Displays the help menu")
async def help(ctx):
    embed = discord.Embed(title="Gato Bot Rewritten", description="A multi-function bot for Discord. Efficient, "
                                                                  "Stable and Customizable.",
                          color=discord.Color.green())
    embed.add_field(name="Moderation", value="`/ban`, `/unban`, `/kick`, `/purge`, `/slowmode`", inline=False)
    embed.add_field(name="Utility", value="`/ping`, `/avatar`, `/serverinfo`, `/userinfo`, `/servericon`, "
                                          "`/serverbanner`, `/stealemoji`, `/slowmode`", inline=False)
    embed.add_field(name="Fun", value="`/8ball`, `/dog`, `/cat`, `/poll`", inline=False)
    embed.add_field(name="Miscellaneous", value="`/reminder`, `/about`, `/invite`", inline=False)
    embed.set_footer(text="Contact: notxofo")
    await ctx.send(embed=embed)

@bot.slash_command(name="invite", description="Displays the invite link for the bot")
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=974318179876749342&permissions=8&scope=bot"
                   "%20applications.commands")


bot.run(token)

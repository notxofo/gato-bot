import discord

bot = discord.Bot(intents=discord.Intents.all())

@bot.command()
async def ban(ctx, usertoban: discord.Option(int), reason: discord.Option(int)):
  await ban(f'{usertoban}, *, reason=p{reason}')

bot.run("TOKEN HERE")
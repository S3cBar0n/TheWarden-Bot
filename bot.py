from discord.ext import commands
import os

client = commands.Bot(command_prefix=commands.when_mentioned_or(">"))


# Loads our cogs library
@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


# Unloads our cogs library
@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(os.environ['TOKEN'])

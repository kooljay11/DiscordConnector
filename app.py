import discord
from discord.ext import commands, tasks
import asyncio
import json


# An overridden version of the Bot class that will listen to the Minecraft server output.
class UnfilteredBot(commands.Bot):
    async def process_commands(self, message):
        ctx = await self.get_context(message)
        await self.invoke(ctx)


client = UnfilteredBot(command_prefix="/", intents=discord.Intents.all())


@client.event
async def on_ready():
    await client.tree.sync()
    print('Bot is ready.')


# Makes a slash command called ping
@client.tree.command(name="ping", description="Shows bot latency in ms.")
async def ping(interaction: discord.Interaction):
    bot_latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! {bot_latency} ms.")


@client.event
async def on_message(message):
    # print(f"message: {message}")
    # print(f"message: {message.content}")

    # Ignore if the sender was this bot
    if message.author.id == 1099535052762787964:
        return

    with open("./channels.txt", "r") as file:
        channels = file.read().split('\n')

    this_channel = str(message.channel.id)
    this_guild = message.guild.id
    sender_name = message.author.name
    try:
        if message.author.discriminator != '0000':
            sender_name += "#" + message.author.discriminator
    except:
        print("No author discriminator.")

    try:
        sender_name = message.author.nick
    except:
        print("No author nick.")

    with open("guild_nicks.json", "r") as file:
        guilds = json.load(file)

    for guild in guilds["nicks"]:
        if this_guild == guild["guild_id"]:
            this_guild = guild["guild_nick"]
            break

    if this_channel in channels:
        channels.remove(this_channel)
        for channel in channels:
            destination_channel = client.get_channel(int(channel))
            await destination_channel.send("[" + this_guild + "] " + sender_name + ": " + message.content)
            # await destination_channel.send("[" + this_guild + "] " + sender_name + ": " + msg)


async def main():
    async with client:
        with open("config.json", "r") as file:
            config = json.load(file)

        await client.start(config['token'])


asyncio.run(main())

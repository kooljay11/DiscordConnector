# https://discord.com/api/oauth2/authorize?client_id=1099535052762787964&permissions=67584&scope=bot
# POTR-notes channel: 801953340736012339
# POTR-bot testing channel: 1058195964491477062
# UBC-commands spam channel: 810664831438684180
import discord
import asyncio
import json

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print('Bot is ready.')


@client.event
async def on_message(message):
    # print(f"message: {message}")
    # guild = await client.fetch_guild(message.guild.id)
    # member = await guild.fetch_member(message.user.id)
    # print(member.nick)
    print(f"message.guild.name: {message.guild.name}")
    print(
        f"message.author.name: {message.author.name}#{message.author.discriminator}")

    print(f"message.channel.id: {message.channel.id}")

    # Ignore if the sender was this bot
    if message.author.id == 1099535052762787964:
        return

    # print(f"message.author.nick: {message.author.nick}")

    with open("./channels.txt", "r") as file:
        # channels = file.readlines()
        channels = file.read().split('\n')

    # print(f"channels: {channels}")
    this_channel = str(message.channel.id)
    this_guild = message.guild.id

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
            await destination_channel.send("[" + this_guild + "] " + message.author.nick + ": " + message.content)
            # await destination_channel.send(message.author.name + "#" + message.author.discriminator + ": " + message.content)


async def main():
    async with client:
        with open("config.json", "r") as file:
            config = json.load(file)

        await client.start(config['token'])


asyncio.run(main())

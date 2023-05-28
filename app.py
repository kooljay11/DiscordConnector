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


# Show all linked channels
@client.tree.command(name="listchannels", description="Lists all linked channels.")
@commands.has_permissions(administrator=True)
async def listchannels(interaction: discord.Interaction):
    if interaction.user.id == 107886996365508608:
        with open("channels.json", "r") as file:
            channels = json.load(file)

        with open("guild_nicks.json", "r") as file:
            guilds = json.load(file)

        output = "All linked channels:\n"

        for channel in channels["channels"]:
            channel_name = client.get_channel(int(channel["channel_id"]))
            guild_name = client.get_guild(int(channel["guild_id"]))
            for guild in guilds["nicks"]:
                if channel["guild_id"] == guild["guild_id"]:
                    guild_name = guild["guild_nick"]
                    break
            output += f"[{guild_name}] #{channel_name}: {channel['channel_id']}\n"

        await interaction.response.send_message(output)
    else:
        await interaction.response.send_message("Cannot run command, because you are not a developer.")


# Remove linked channel
@client.tree.command(name="rmchannel", description="Removes a linked channel.")
@commands.has_permissions(administrator=True)
async def rmchannel(interaction: discord.Interaction, channel_id: str):
    if interaction.user.id == 107886996365508608:
        with open("channels.json", "r") as file:
            channels = json.load(file)

        for channel in channels["channels"]:
            if channel["channel_id"] == int(channel_id):
                channels["channels"].remove(channel)
                break

        with open("channels.json", "w") as file:
            json.dump(channels, file, indent=4)

        await interaction.response.send_message("Success.")
    else:
        await interaction.response.send_message("Cannot run command, because you are not a developer.")


# Add a linked channel
@client.tree.command(name="addchannel", description="Adds a linked channel.")
@commands.has_permissions(administrator=True)
async def addchannel(interaction: discord.Interaction, channel_id: str, guild_id: str):
    if interaction.user.id == 107886996365508608:
        with open("channels.json", "r") as file:
            channels = json.load(file)

        channel = {
            "guild_id": int(guild_id),
            "channel_id": int(channel_id)
        }
        channels["channels"].append(channel)

        with open("channels.json", "w") as file:
            json.dump(channels, file, indent=4)

        await interaction.response.send_message("Success.")
    else:
        await interaction.response.send_message("Cannot run command, because you are not a developer.")


# Show all linked channels
@client.tree.command(name="listguildnicks", description="Lists all guild nicks.")
@commands.has_permissions(administrator=True)
async def listguildnicks(interaction: discord.Interaction):
    if interaction.user.id == 107886996365508608:
        with open("guild_nicks.json", "r") as file:
            guilds = json.load(file)

        output = "All guild nicks:\n"

        for guild in guilds["nicks"]:
            guild_nick = guild["guild_nick"]
            guild_id = int(guild["guild_id"])
            output += f"{guild_nick}: {guild_id}\n"

        await interaction.response.send_message(output)
    else:
        await interaction.response.send_message("Cannot run command, because you are not a developer.")


# Remove guild nick
@client.tree.command(name="rmguildnick", description="Removes a guild nick.")
@commands.has_permissions(administrator=True)
async def rmguildnick(interaction: discord.Interaction, guild_id: str):
    if interaction.user.id == 107886996365508608:
        with open("guild_nicks.json", "r") as file:
            guilds = json.load(file)

        for guild in guilds["nicks"]:
            if guild["guild_id"] == int(guild_id):
                guilds["nicks"].remove(guild)
                break

        with open("guild_nicks.json", "w") as file:
            json.dump(guilds, file, indent=4)

        await interaction.response.send_message("Success.")
    else:
        await interaction.response.send_message("Cannot run command, because you are not a developer.")


# Add a linked channel
@client.tree.command(name="addguildnick", description="Adds a guild nick.")
@commands.has_permissions(administrator=True)
async def addguildnick(interaction: discord.Interaction, guild_id: str, guild_nick: str):
    if interaction.user.id == 107886996365508608:
        with open("guild_nicks.json", "r") as file:
            guilds = json.load(file)

        guild = {
            "guild_id": int(guild_id),
            "guild_nick": guild_nick
        }
        guilds["nicks"].append(guild)

        with open("guild_nicks.json", "w") as file:
            json.dump(guilds, file, indent=4)

        await interaction.response.send_message("Success.")
    else:
        await interaction.response.send_message("Cannot run command, because you are not a developer.")


@client.event
async def on_message(message):
    # Ignore if the sender was this bot
    if message.author.id == 1099535052762787964:
        # print("Ignoring self.")
        return

    with open("channels.json", "r") as file:
        channels = json.load(file)

    # this_channel = str(message.channel.id)
    this_guild = message.guild.id
    this_channel = {
        "guild_id": message.guild.id,
        "channel_id": message.channel.id
    }
    sender_name = message.author.name
    try:
        if message.author.discriminator != '0000':
            sender_name += "#" + message.author.discriminator
    except:
        # print("No author discriminator.")
        print("")

    try:
        sender_name = message.author.nick
    except:
        # print("No author nick.")
        print("")

    with open("guild_nicks.json", "r") as file:
        guilds = json.load(file)

    for guild in guilds["nicks"]:
        if this_guild == guild["guild_id"]:
            this_guild = guild["guild_nick"]
            break

    if this_channel in channels["channels"]:
        channels["channels"].remove(this_channel)
        for channel in channels["channels"]:
            destination_channel = client.get_guild(
                channel['guild_id']).get_channel(channel['channel_id'])
            await destination_channel.send("[" + this_guild + "] " + sender_name + ": " + message.content)


async def main():
    async with client:
        with open("config.json", "r") as file:
            config = json.load(file)

        await client.start(config['token'])


asyncio.run(main())

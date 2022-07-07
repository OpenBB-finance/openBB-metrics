import asyncio
import discord
import requests
from utilities.config import settings

def get_active_members():
    url = 'https://discord.com/api/guilds/831165782750789672/widget.json'
    r = requests.get(url)
    data = r.json()
    active_members = data['presence_count']
    print(active_members)

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

def filterOnlyBots(member):
    return member.bot

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    server_id = 831165782750789672
    guild = client.get_guild(server_id)
    memberList = guild.members
    botsInServer = list(filter(filterOnlyBots, memberList))
    for bot in botsInServer:
        print(bot)
    botsInServerCount = len(botsInServer)
    # (Total Member count - bot count) = Total user count
    usersInServerCount = guild.member_count - botsInServerCount
    print(botsInServerCount, usersInServerCount)
    loop = asyncio.get_running_loop()
    loop.stop()


def get_members():
    client.run(settings.YOUTUBE_TOKEN)
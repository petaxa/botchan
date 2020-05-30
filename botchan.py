import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import os

token = os.environ['DISCORD_BOT_TOKEN']

jst = datetime.utcnow() + timedelta(hours=9)
hour = f'{jst:%H}'
minute = f'{jst:%M}'

client = commands.Bot(command_prefix='.')
# client = discord.Client()
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


#入出管理
@client.event
async def on_voice_state_update(member, before, after):
    himitsu = client.get_channel(671764452646977538)
    if member.guild.id == 454634464174407681 and (before.channel != after.channel):
        now = datetime.utcnow() + timedelta(hours=9)
        alert_channel = client.get_channel(639850501780930580)
        secret = client.get_channel(672052787411943434)
        if after.channel == himitsu and before.channel is None:
            msg = f'{now:%m/%d-%H:%M} に {member.name} が {after.channel.name} に参加しました。'
            await secret.send(msg)
        elif before.channel == himitsu and after.channel is None:
            str = f'{now:%m/%d-%H:%M} に {member.name} が {before.channel.name} から退出しました。'
            await secret.send(str)
        else:
            if before.channel is None:
                msg = f'{now:%m/%d-%H:%M} に {member.name} が {after.channel.name} に参加しました。'
                await alert_channel.send(msg)
            elif after.channel is None:
                msg = f'{now:%m/%d-%H:%M} に {member.name} が {before.channel.name} から退出しました。'
                await alert_channel.send(msg)
        


client.run(token)

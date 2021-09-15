import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import os

token = os.environ['DISCORD_BOT_TOKEN']

client = commands.Bot(command_prefix='.')
# client = discord.Client()
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#お遊びメッセージ
@client.command()
async def yui(arg):
    yuichan = discord.Embed(title='わたしはカーディナルに存在するAIです。', description='**名前はbotchanです。仲良くしてね。**', color=46121)
    yuichan.add_field(name='**機能紹介**',value='利用できる機能を紹介します',inline=False)
    yuichan.add_field(name='**.rect 募集内容 募集人数 終了までの時間(秒)**',value="パーティメンバーを募集できます")
    yuichan.add_field(name='**.weapon**',value='熟練度を開始します。また、「熟練中」の役職を付与します。')
    yuichan.add_field(name='**.end 獲得経験値 時間 分**',value='獲得情報をまとめ、時給を計算します。')
    yuichan.add_field(name="**vc入出管理**", value="vcに入出した時に#enter-exit-logsに記録されます",inline=False)
    yuichan.add_field(name='botの機能募集してます|ω・`）',value='何かあったらお声掛けください。できるかはわかりませんが()',inline=False)
    yuichan.add_field(name='意地悪はしないでください',value=':rage: ')
    await arg.channel.send(embed=yuichan)

@client.command()
async def papa(dad):
    await dad.send('ぱぱ〜')
@client.command()
async def mama(mam):
    await mam.send('まま〜')


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
      elif member.guild.id == 884594072130560120 and (before.channel != after.channel):
        now = datetime.utcnow() + timedelta(hours=9)
        alert_channel_M = client.get_channel(887357758523985920)
        if after.channel == before.channel is None:
            msg = f'{now:%m/%d-%H:%M} に {member.name} が {after.channel.name} に参加しました。'
            await alert_channel_M.send(msg)
        elif before.channel == after.channel is None:
            str = f'{now:%m/%d-%H:%M} に {member.name} が {before.channel.name} から退出しました。'
            await alert_channel_M.send(str)
        
        

jst = datetime.utcnow() + timedelta(hours=9)
hour = f'{jst:%H}'
minute = f'{jst:%M}'

#熟練度計算
@client.command()
async def weapon(buki,exp='秘密'):
    role = buki.guild.get_role(640846203361165332)
    user_role = buki.author.roles
    print(user_role)
    # print(role)
    if role not in buki.author.roles:
        text = f'{hour}:{minute}に{buki.author.name}が熟練度を開始しました'
        now = f'現在の経験値は{exp}です'
        await buki.send(text)
        await buki.send(now)
        # start_jkr = discord.utils.get(buki.guild.roles, id=640846203361165332)
        await buki.author.add_roles(role)
    else:
        dame_text = 'エラーですよ'
        await buki.channel.send(dame_text)



@client.command()
async def end(owari,kakutoku=None,jikan=None,hun=None):
    role = owari.guild.get_role(640846203361165332)
    user_role = owari.author.roles
    if role in user_role:
        end_text = f'{hour}:{minute}に{owari.author.name}が熟練度を終了しました'
        await owari.send(end_text)
        role = discord.utils.get(owari.guild.roles, name='熟練中')
        await owari.author.remove_roles(role)
        end_embed = discord.Embed(title='⚔️RESULT⚔️',description='今回の熟練度の...', color=0xFF1A6F)
        if int(hun) > 60:
            over_jikan = int(jikan) + round(int(hun) / 60)
            over_hun = int(hun) % 60
            text_kakutoku, text_jikan, text_hun = str(kakutoku),str(over_jikan),str(over_hun)
            cal_kakutoku, cal_jikan, cal_hun = int(kakutoku),float(jikan),float(int(over_hun)/60)
            jikyu = round(cal_kakutoku / (cal_jikan + cal_hun),3)
            end_embed.add_field(name='プレイ時間', value=f"{text_jikan}時間{text_hun}分でした")
            end_embed.add_field(name='獲得経験値', value=f'{text_kakutoku}ポイント獲得しました')
            end_embed.add_field(name='時給',value=f'1時間で{jikyu}ポイント稼ぎました')
            bato_text = '1時間は60分です。小学生からやり直してきてください。'
            await owari.channel.send(embed=end_embed)
            await owari.channel.send(bato_text)
        else:
            text_kakutoku,text_jikan,text_hun = str(kakutoku),str(jikan),str(hun)
            cal_kakutoku,cal_jikan,cal_hun = int(kakutoku),float(jikan),float(int(hun)/60)
            jikyu = round(cal_kakutoku / (cal_jikan + cal_hun),3)
            end_embed.add_field(name='プレイ時間', value=f"{text_jikan}時間{text_hun}分でした")
            end_embed.add_field(name='獲得経験値', value=f'{text_kakutoku}ポイント獲得しました')
            end_embed.add_field(name='時給', value=f'一時間で{jikyu}ポイント稼ぎました')
            await owari.channel.send(embed=end_embed)
    else:
        error_text = 'まだ開始していません'
        await owari.channel.send(error_text)

#実験
@client.command()
async def should(should):
    yarukoto = discord.Embed(title='やることリスト',color=0xA16EFF)
    yarukoto.add_field(name='熟練度計算ツールのEmbed化',value='結果をEmbed化して見やすくしたい：結果の埋め込みはできた')
    yarukoto.add_field(name='熟練度計算ツールのレベルアップに対応', value='計測中にレベルアップしても計算を可能にしたい。')
    yarukoto.add_field(name='help機能の充実',value='コマンドの使い方をもっと詳しく。できればリアクションによるページの遷移も。')
    yarukoto.add_field(name='ランウォッチ機能',value='引数に距離と時間をいれ、時速と消費カロリーを返す。\n初期コマンドを作ってそこで個人チャンネルを作ればDBみたいになるかな？')
    await should.channel.send(embed=yarukoto)

@client.command()
async def null(null):
    people = 0
    for member in null.guild.members:
        if not member.bot:
            role = discord.utils.get(null.guild.roles,name='null')
            await member.add_roles(role)
            people += 1
    text = f'{people}人のメンバーに役職を付与できました'
    await null.channel.send(text)

@client.command()
async def devide(devide):
    for member in devide.guild.members:
        if member.bot:
            role = discord.utils.get(devide.guild.roles,name='bot')
            await member.add_roles(role)
    text = 'botに役職を付与できました'
    await devide.channel.send(text)

@client.command()
async def D(ctx):
    for user in ctx.guild.members:
        if user.status == discord.Status.online:
            print (user.name+"#"+user.discriminator)
            
#匿名メッセージ
@client.event
async def on_message(message):
    if message.author.bot:
        # もし、送信者がbotなら無視する
        return
    GLOBAL_CH_NAME = "hoge-global" # グローバルチャットのチャンネル名

    if message.channel.name == GLOBAL_CH_NAME:
        # hoge-globalの名前をもつチャンネルに投稿されたので、メッセージを転送する

        await message.delete() # 元のメッセージは削除しておく

        channels = client.get_all_channels()
        print(channels)
        global_channels = [ch for ch in channels if ch.name == GLOBAL_CH_NAME]
        # channelsはbotの取得できるチャンネルのイテレーター
        # global_channelsは hoge-global の名前を持つチャンネルのリスト

        embed = discord.Embed(title="hoge-global",
            description=message.content, color=0x00bfff)

        embed.set_author(name=message.author.display_name,
            icon_url=message.author.avatar_url_as(format="png"))
        embed.set_footer(text=f"{message.guild.name} / {message.channel.name}",
            icon_url=message.guild.icon_url_as(format="png"))
        # Embedインスタンスを生成、投稿者、投稿場所などの設定

        for channel in global_channels:
            print(global_channels)
            # メッセージを埋め込み形式で転送
            await channel.send(embed=embed)
            
@client.command()
async def biginning(bigin):
    bigining = discord.Embed(title='ようこそてんぺすとのお部屋へ！',description='以下の文章をお読みになってから先へ進んでくださいませ。',color=0xf0f8ff)
    bigining.add_field(name='Rule',value='基本的に何しても自由ですが、常識の範囲内でお願いします。\nあまりにも私の常識と乖離していると感じた場合はBAN等の措置を執らせていただく場合が\nございます')
    bigining.add_field(name="チャンネル説明",value='-------------------------------',inline=False)
    bigining.add_field(name='main-chat',value='雑談等は[#main-chat](https://discordapp.com/channels/454634464174407681/583951802630668288)をご利用ください')
    bigining.add_field(name='saoif-info',value='[#saoif-news](https://discordapp.com/channels/454634464174407681/634780447250972685)、[#japan-server-news](https://discordapp.com/channels/454634464174407681/641515191569481729)にてsaoifの\n情報を掲載しています')
    bigining.add_field(name='聞き専',value='vc時にメッセージをやり取りする場合は[#listening-chat](https://discordapp.com/channels/454634464174407681/583951396114530306)、をご利用ください')
    bigining.add_field(name='voice-chat',value='vcはmain-vcをご利用ください')
    bigining.add_field(name='bot-spam',value='それぞれにbotの名前がついておりますので\n対応したものをお使いください。')
    bigining.add_field(name='入出管理',value='vcに出入りした時に日時を記録してくれます')
    bigining.add_field(name='導入bot',value='[@Yui](https://discordapp.com/channels/@me/580071590738264065):saoif全般の情報を引き出せます。\n[@Rythm](https://discordapp.com/channels/@me/440105191992459266):接続中のvcに音楽を流せます\n[@botchan](https://discordapp.com/channels/@me/440105191992459266):私が勉強がてら頑張ってる自作botです「.yui」で機能を表示します')
    await bigin.channel.send(embed=bigining)


client.run(token)

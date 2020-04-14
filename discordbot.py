import discord
from discord.ext import tasks
from datetime import datetime
import jpholiday
import locale

locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")

client = discord.Client()
channel = None
done = False

yobi = ["月","火","水","木","金","土","日"]
channelId = os.environ['DISCORD_CHANNEL_ID']
token = os.environ['DISCORD_BOT_TOKEN']

workStart = '22:45'
breakStart = '22:50'
breakEnd = '22:55'
workEnd = '23:00'

weekDay = yobi[datetime.now().weekday()]
nowStr = datetime.now().strftime('%Y年%m月%d日') + ' (' + weekDay + ')'

@client.event
async def on_ready():
    print('----------------')
    print('ログインしました')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('----------------')
    global channel
    channel = client.get_channel(channelId)
    loop.start()


# 60秒に一回ループ
@tasks.loop(seconds=20)
async def loop():
    if isBizDay():
        global done
        # 現在の時刻
        now = datetime.now().strftime('%H:%M')
        print(now)
        print(done)
        print('----------------')

        if now == workStart:
            if not done:
                await channel.send('おはようございます。就業開始です。\n本日は ' + nowStr + '\n忘れずにメールしましょう。')
                done = True
        elif now == breakStart:
            if not done:
                await channel.send('お疲れさまです。休憩開始です。\n忘れずにメールしましょう。')
                done = True
        elif now == breakEnd:
            if not done:
                await channel.send('お疲れさまです。休憩終了です。\n忘れずにメールしましょう。')
                done = True
        elif now == workEnd:
            if not done:
                await channel.send('お疲れさまでした。就業終了です。\n忘れずにメールしましょう。')
                done = True
        else:
            done = False


@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/ping':
        await message.channel.send('成功')


def isBizDay():
    Date = datetime.now()
    # tstr = '2020-04-29 00:00:00'
    # Date = datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')
    if Date.weekday() >= 5 or jpholiday.is_holiday(Date):
        return False
    else:
        return True


client.run(token)
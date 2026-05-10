import discord
from discord.ext import commands
import random

TOKEN = "MTUwMzEwODkwMjIzNjA2NTc5Mg.GCmPwj.D7W0AgnPpCXMKehUXtSaU0fT3X48meMz4HOhV4"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

pot = 10000000
tickets = []

@bot.event
async def on_ready():
    print(f"✅ 已登入：{bot.user}")
@bot.command()
async def alltickets(ctx):

    global tickets

    if len(tickets) == 0:

        await ctx.send("❌ 目前沒有人購買彩票")
        return

    players = {}

    for ticket in tickets:

        player = ticket["player"]

        if player not in players:

            players[player] = 0

        players[player] += 1

    result = "🎰【黑金樂透總覽】\n\n"

    total_tickets = 0
    total_money = 0

    for player, count in players.items():

        money = count * 20000

        total_tickets += count
        total_money += money

        result += (
            f"👤 {player}\n"
            f"🎟 張數：{count}\n"
            f"💰 投入：{money:,}\n\n"
        )

    result += (
        f"━━━━━━━━━━\n"
        f"🎟 總張數：{total_tickets}\n"
        f"💰 總獎池增加：{total_money:,}"
    )

    await ctx.send(result)
@bot.command()
async def playertickets(ctx, player):

    global tickets

    player_tickets = []

    for ticket in tickets:

        if ticket["player"] == player:

            player_tickets.append(ticket)

    count = len(player_tickets)
    total = count * 20000

    if count == 0:

        await ctx.send("❌ 查無此玩家彩票")
        return

    result = (
        f"🎟 玩家：{player}\n"
        f"購買張數：{count} 張\n"
        f"投入金額：{total:,} 遊戲幣\n\n"
        f"號碼：\n"
    )

    for t in player_tickets:

        result += f"{t['numbers']}\n"

    await ctx.send(result)
async def potshow(ctx):
    global pot

    await ctx.send(
        f"🎰【黑金樂透】\n"
        f"目前獎池：{pot:,} 遊戲幣"
    )

@bot.command()
async def addticket(ctx, player, n1:int, n2:int, n3:int, n4:int, n5:int):
    global pot
    global tickets

    numbers = [n1, n2, n3, n4, n5]

    tickets.append({
        "player": player,
        "numbers": numbers
    })

    pot += 20000

    await ctx.send(
        f"✅ 已新增彩票\n"
        f"玩家：{player}\n"
        f"號碼：{numbers}\n"
        f"目前獎池：{pot:,}"
    )

@bot.command()
async def draw(ctx):

    global pot
    global tickets

    winning = random.sample(range(1,21),5)

    result = (
        f"🎰【黑金樂透開獎】🎰\n\n"
        f"本期號碼：\n"
        f"{winning}\n\n"
    )

    winners = []

    for ticket in tickets:

        if ticket["numbers"] == winning:

            winners.append(ticket["player"])

    if winners:

        reward = int(pot * 0.5 / len(winners))

        result += "🏆 頭獎得主：\n"

        for w in winners:
            result += f"{w}\n"

        result += f"\n每人獲得：{reward:,} 遊戲幣"

    else:

        result += "❌ 本期無人中頭獎\n"
        result += "彩金累積至下期"

    await ctx.send(result)

bot.run(TOKEN)

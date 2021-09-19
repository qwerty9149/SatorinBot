import discord
from discord.ext import commands, tasks
import os
import logging
import requests
import time
from itertools import cycle
from keep_alive import keep_alive
import random
import asyncio
import cloudscraper
from bs4 import BeautifulSoup
import re

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="!", help_command=None)

@bot.command()
async def wacca(ctx, a, b, c, d):
    ma = int(a)
    gr = int(b)
    go = int(c)
    mi = int(d)
    ncount = int(ma + gr + go + mi)
    nscore = 1000000 / ncount
    grscore = nscore * (0.7)
    goscore = nscore * (0.5)
    total = round(ma * nscore + gr * grscore + go * goscore)
    grade = ""
    if total == 1000000:
      grade = ":regional_indicator_a: :regional_indicator_m: :tada:"
    elif total >= 990000:
       grade = ":regional_indicator_s: :regional_indicator_s: :regional_indicator_s: ＋"
    elif total >= 980000:
       grade = ":regional_indicator_s: :regional_indicator_s: :regional_indicator_s:"
    elif total >= 970000:
       grade = ":regional_indicator_s: :regional_indicator_s: ＋"
    elif total >= 950000:
       grade = ":regional_indicator_s: :regional_indicator_s:"
    elif total >= 930000:
       grade = ":regional_indicator_s: ＋"
    elif total >= 900000:
       grade = ":regional_indicator_s:"
    elif total >= 850000:
       grade = ":a: :a: :a:"
    elif total >= 800000:
        grade = ":a: :a:"
    elif total >= 700000:
        grade = ":a:"
    elif total >= 300000:
        grade = ":b:"
    elif total >= 1:
        grade = ":regional_indicator_c:"
    else:
        grade = ":regional_indicator_d:"

    if (gr + go + mi) == 0:
         hyoka = " All Marvelous!"
    elif mi == 0:
         hyoka = " Full Combo!"
    elif mi <= 5:
         hyoka = " Missless!"
    else:
         hyoka = ""

    await ctx.channel.send("Your score is:\n" + grade + "\n" + "**" + str(total) + " " + hyoka + "**")

@bot.command()
async def waccar(ctx, a, b, c, d, e, f, g, h):
    ma = int(a)
    gr = int(b)
    go = int(c)
    mi = int(d)
    rma = int(e)
    rgr = int(f)
    rgo = int(g)
    rmi = int(h)
    ncount = int(ma + gr + go + mi + rma + rgr + rgo + rmi)
    nscore = 1000000 / ncount
    grscore = nscore * (0.7)
    goscore = nscore * (0.5)
    if (ma < rma) or (gr < rgr) or (go < rgo) or (mi < rmi):
        await ctx.channel.send("Incorrect input ah on9!")
    else:
        total = round((ma + rma) * nscore + (gr + rgr) * grscore + (go + rgo) * goscore)
        grade = ""

        if total == 1000000:
            grade = ":regional_indicator_a: :regional_indicator_m: :tada:"
        elif total >= 990000:
            grade = ":regional_indicator_s: :regional_indicator_s: :regional_indicator_s: ＋"
        elif total >= 980000:
            grade = ":regional_indicator_s: :regional_indicator_s: :regional_indicator_s:"
        elif total >= 970000:
            grade = ":regional_indicator_s: :regional_indicator_s: ＋"
        elif total >= 950000:
            grade = ":regional_indicator_s: :regional_indicator_s:"
        elif total >= 930000:
            grade = ":regional_indicator_s: ＋"
        elif total >= 900000:
            grade = ":regional_indicator_s:"
        elif total >= 850000:
            grade = ":a: :a: :a:"
        elif total >= 800000:
            grade = ":a: :a:"
        elif total >= 700000:
            grade = ":a:"
        elif total >= 300000:
            grade = ":b:"
        elif total >= 1:
            grade = ":regional_indicator_c:"
        else:
            grade = ":regional_indicator_d:"

        if (gr + go + mi) == 0:
            hyoka = " All Marvelous!"
        elif mi == 0:
            hyoka = " Full Combo!"
        elif mi <= 5:
            hyoka = " Missless!"
        else:
            hyoka = ""

        await ctx.channel.send("Your score is:\n" + grade + "\n" + "**" + str(total) + " " + hyoka + "**")


@bot.command()
async def ping(ctx, arg=""):
    await ctx.channel.send("pong")

@bot.command()
async def timenow(ctx, arg=""):
  newhour = str((int(time.strftime("%H")) + 8) % 24).zfill(2) #some timezone awfulness lmfao
  await ctx.channel.send(str(newhour) + time.strftime(":%M:%S"))

@bot.command()
async def help(context):
    await context.send(
        "__**!wacca**__: input your scores in the form `!wacca a b c d`, where:\na: Marvelous notes\nb: Great notes\nc: Good notes\nd: Miss notes\n\n__**!waccar**__: input your scores in the form `!waccar a b c d e f g h`, where:\na: Marvelous notes\nb: Great notes\nc: Good notes\nd: Miss notes\ne: Marvelous R notes\nf: Great R notes\ng: Good R notes\nh: Miss R notes\n\n__**!ping**__: pong (makes sure bot isn't dead)\n\n__**!guya n**__: pings manatoki every minute to check for kaguya-sama KR scan of chapter n (n < 10), pings @masahiro with link if scan is out (unstoppable and disables bot, beware; prone to random crashes after a few dozen few hundred reps)\n\n__**!zaibatsu n**__: same as above but with zaibatsu on guya.moe instead\n\n__**!rand n**__: randomly generates integer from 1 to n\n\n__**!timenow**__: displays current time in HKT"
    )


@bot.command()
async def guya(ctx, c):
    chno = str(int(c) - 10)
    whereguya = " " + chno + "화"
    i = 0
    while i > -1:
        scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
        }) 
        txt = scraper.get("https://manatoki106.net/comic/118798").text
        x = txt.find(whereguya)
        if x != -1:
          soup = BeautifulSoup(txt, "html.parser")
          links = soup.find_all('a')
          for link in links:
            if link.find(text=re.compile(whereguya)):
              thelink = link
              break
          await ctx.channel.send("new guya pog <@371125260634030080>\n" + thelink.get('href')[:-8] + "\ncompleted in " + str(i) + " reps")
          break
        newhour = str((int(time.strftime("%H")) + 8) % 24).zfill(2)
        await ctx.channel.send("still no new guya at time " + str(newhour) + time.strftime(":%M:%S") + "; rep number: " + str(i), delete_after=60)
        await asyncio.sleep(60)
        i += 1

@bot.command()
async def zaibatsu(ctx, c):
 chno = c
 i = 0
 while i > -1:
        headers = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        }
        cookies = dict(cookies_are='working')
        r = requests.get(
            "https://guya.moe/read/manga/Kaguya-Wants-To-Be-Confessed-To/" + chno + "/1/",
            headers=headers,
            cookies=cookies)
        code = int(r.status_code)
        if code == 200:
          await ctx.channel.send("new zaibatsu pog <@371125260634030080>\nhttps://guya.moe/read/manga/Kaguya-Wants-To-Be-Confessed-To/" + str(chno) + "/1/\n\ncompleted in " + str(i) + " reps")
          break
        newhour = str((int(time.strftime("%H")) + 8) % 24).zfill(2)
        await ctx.channel.send("still no new zaibatsu at time " + str(newhour) + time.strftime(":%M:%S") + "; rep number: " + str(i), delete_after=60)
        await asyncio.sleep(60)
        i += 1

status = cycle(["haha bot goes brrrr", "bot is deadn't, pog"])

keep_alive()

@bot.event
async def on_ready():
  change_status.start()
  print('Logging in as {0.user}'.format(bot) + '...')

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))

@bot.command()
async def rand(ctx, n):
  try:
    bruh = int(n)
    randresult = random.randint(1,bruh)
    await ctx.channel.send(str(randresult))
  except ValueError:
    await ctx.channel.send("Needs an integer ah 7head!")
  
bot.run(os.getenv('TOKEN'))

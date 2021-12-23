id='verify role id'
token='your token'


from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
import discord,os,asyncio
from secrets import token_hex
from random import randint
intents = discord.Intents().all()
bot = commands.Bot(intents=intents, help_command=None)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

@bot.slash_command()
async def verify(ctx):
    if ctx.guild != None:
        await ctx.respond("use in dm")
        return
    img = Image.new("RGB", (300, 100), color="white")
    d1 = ImageDraw.Draw(img)
    myFont = ImageFont.truetype("verify.ttf", 50)
    texts = str(token_hex()[0:5])
    for i, text in enumerate(texts):
        d1.text(
            (25 + i * randint(40, 50), 25),
            text,
            font=myFont,
            fill=(randint(0, 200), randint(0, 200), randint(0, 200)),
        )
    for i in range(100):
        place = randint(20, 250)
        place2 = randint(20, 80)
        d1.ellipse(
            (place, place2, place + 3, place2 + 3),
            fill=(randint(0, 200), randint(0, 200), randint(0, 200)),
        )
    img = img.rotate(angle=randint(1, 15))
    if os.path.exists("verify.jpg"):
        os.remove("verify.jpg")
    img.save("verify.jpg")
    await ctx.respond(file=discord.File("verify.jpg"), content="請輸入驗證碼")
    os.remove("verify.jpg")

    def check(msg):
        if msg.author == ctx.author and msg.guild == None:
            if texts in msg.content:
                return True
            else:
                return False
        else:
            return False

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        return await ctx.send("verify fall")
    else:
        await ctx.send("verify success")
        await bot.guilds[0].get_member(ctx.author.id).add_roles(
            bot.guilds[0].get_role(id)
        )
        
bot.run(token)

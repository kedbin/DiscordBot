#!/usr/bin/python3
import discord
from Credentials import token, discordId
from discord.ext import commands
import os
import requests
import random
import datetime

client = commands.Bot(command_prefix = '.')

def is_k3dbin():
    async def predicate(ctx):
        if ctx.author.id not in discordId:
            await ctx.send("To prevent a certain someone *cough* MONDYS *cough* from uploading a certain sleeping photo. \
This command has been restricted. You cannot use this function.")
            return 0
        return 1
    return commands.check(predicate)

@client.event
async def on_ready():
    print("Bot is ready.")

def saveImg(r, imageName):
    with open(imageName, 'wb') as out_file:
        print('Saving image..')
        out_file.write(r.content)

@client.command()
@is_k3dbin()
async def save(ctx, directory, description=None):
    try:
        url = ctx.message.attachments[0].url
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":
            r = requests.get(url, stream=True)
            contentName = url[39:].split("/")[-1]
            imageName = f"{directory.lower()}/{contentName}"
            try:
                saveImg(r, imageName)
            except FileNotFoundError:
                os.mkdir(directory.lower())
                print("Directory Made!")
                saveImg(r,imageName)
                await ctx.send("Directory Created!")
            finally:
                await ctx.send("Attachment Saved!")

    with open(f"{directory.lower()}/.dict", "a+") as file:
        file.write(f"{contentName}---{description} (Added @ {datetime.datetime.now()}) \n")
    if description == None:
        await ctx.send("No Description given.")
    else:
        await ctx.send("Description Saved!")

@client.command(aliases=["cmu","cheer"])
async def cheermeup(ctx, idol=None):
    d = {}
    if idol == None:
        idol = random.choice([folder for folder in os.listdir() if not os.path.isfile(folder) and folder[0] != "." and folder[0] != "_"])
        await ctx.send(f"No name provided, randomly chosen {idol.capitalize()} for you. Enjoy ;)")
    try:
        files = [file for file in os.listdir(idol.lower()) if os.path.isfile(f"{idol.lower()}/{file}") and file[0] != "."]
        choice = random.choice(files)
        filePath = f"{idol.lower()}/{choice}"
        print(f"The file chosen was {filePath}")
        with open(filePath, "rb") as fh:
            fileToSend = discord.File(fh, filename=choice)

    except FileNotFoundError:
        await ctx.send("There is no saved category under that name. Pls use '.names' to view available ones")

    with open(f"{idol.lower()}/.dict", "r") as descriptionDictionary:
        for line in descriptionDictionary:
            (key,val) = line.split("---")
            d[key] = val
    
    await ctx.send(file=fileToSend)
    await ctx.send(f"{d[choice]}")


@client.command(aliases=["name","who"])
async def names(ctx):
    files = [ f for f in os.listdir() if not os.path.isfile(f) and f[0] != "_" and f[0] != "."]
    await ctx.send(f"The available categories are as follows")
    for i in files:
        await ctx.send(i.capitalize())

@client.event
async def on_message(message):
    if message.content.lower() in ["iloveyou", "iloveyou bot", "ilybot", "ilysm", "bestbot","iloveyoubot","i love you", "thankyou"]:
        await message.channel.send(random.choice(["Mou!! Hazukashii >wwwww<. ;* ", "W-w-what are you saying?! BAKAAAAA!!! b-b-but thanks O////O",
        "I am but a bot uncapable of love x(", "H-h-hontou?? >////< I'm so happy to hear that from you, senpai.. I like you too",
        "BAKAAAAAAAAA! Not in public >www<" ]))
    await client.process_commands(message)


client.run(token)
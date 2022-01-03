#!/usr/bin/python3
import discord
from Credentials import token
from discord.ext import commands
import os
import requests
import random
import datetime

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print("Bot is ready.")

def saveImg(r, imageName):
    with open(imageName, 'wb') as out_file:
        print('Saving image..')
        out_file.write(r.content)

@client.command()
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
        await ctx.send("Please add a name!")
        return
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

client.run(token)
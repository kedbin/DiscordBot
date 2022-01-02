#!/usr/bin/python3
import discord
from Credentials import token
from discord.ext import commands
import os
import requests

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print("Bot is ready.")

def saveImg(r, imageName):
    with open(imageName, 'wb') as out_file:
        print('Saving image..')
        out_file.write(r.content)

@client.command()
async def save(ctx, directory):
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


client.run(token)
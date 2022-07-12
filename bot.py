import asyncio
from xmlrpc.client import boolean # Why?

import discord
# from discord.ext import commands
from discord.commands import Option

from question_lists import QuestionList

token = 'REPLACE WITH TOKEN'
guild_id = 'REPLACE WITH GUILD ID (INT, NOT STR)'

intents = discord.Intents.default()
intents.members = True
# intents.message_content = True

description = "Q, omnipotent being and asker of questions."
bot = discord.Bot(description=description, intents=intents)

asked = QuestionList("asked_" + str(guild_id))
unasked = QuestionList("unasked_" + str(guild_id))

@bot.event
async def on_ready():
    print(f"I have entered this reality as {bot.user} (ID: {bot.user.id})")
    print("----------")

@bot.slash_command(guild_ids=[guild_id])
async def add(ctx: discord.ApplicationContext, text: str, author: str):
    question = unasked.make_question(author, text)
    unasked.add(question)

@bot.slash_command(guild_ids=[guild_id])
async def remove(ctx: discord.ApplicationContext, question_id: int):
    unasked.remove(question_id)

@bot.slash_command(guild_ids=[guild_id])
async def move(ctx: discord.ApplicationContext, question_id: int):
    question = unasked.remove(question_id)
    asked.add(question)

@bot.slash_command(guild_ids=[guild_id])
async def list(ctx: discord.ApplicationContext):
    questions = unasked.list()

    await ctx.send(questions)

bot.run(token)

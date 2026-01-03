import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import routes.home

pedido = routes.home.pedido

load_dotenv()
TOKEN = os.getenv('CHAVE')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')




bot.run(TOKEN)
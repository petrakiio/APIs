#bot pra gerenciar os sistemas de pedidos via discord

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connection.pedidos import pedido_entrege

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name='entregar')
async def entregar(ctx, codigo_pedido: int):
    sucesso = pedido_entrege(codigo_pedido)
    if sucesso:
        await ctx.send(f'Pedido {codigo_pedido} marcado como entregue.')
    else:
        await ctx.send(f'Falha ao marcar o pedido {codigo_pedido} como entregue. Verifique o código e tente novamente.')

bot.run(TOKEN)
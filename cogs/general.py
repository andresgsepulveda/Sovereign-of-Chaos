##############################################
# Package Imports
##############################################
import random
import sys

import discord 
from discord.ext import commands
from discord.ext.commands import Bot, Context

from log import ConsoleLog

LAUGH_TRACK_LINK = "https://www.youtube.com/watch?v=J83lw0eFIJA"

##############################################
# Constants and Setup
##############################################
answers = [
  'It is certain.', 
  'It is decidedly so.',
  'You may rely on it.',
  'Without a doubt.',
  'Yes - definitely.', 
  'As I see, yes.', 
  'Most likely.', 
  'Outlook good.', 
  'Yes.',
  'Signs point to yes.',
  'Reply hazy, try again.', 
  'Ask again later.', 
  'Better not tell you now.',
  'Cannot predict now.',
  'Concentrate and ask again later.', 
  'Don\'t count on it.',
  'My reply is no.',
  'My sources say no.', 
  'Outlook not so good.', 
  'Very doubtful.'
]

HELP_LINK = "https://sovereign-of-chaos.anvil.app"

MODULE = "GENERAL"

class General( commands.Cog, name = "General" ):

  ##############################################
  # General Cog Initialization
  ##############################################
  def __init__( self, bot: Bot ):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message( self, msg: Message) -> None:

    if msg.author.bot or msg.author == self.bot.user:
      return 

    content = msg.content 
    if "/j" not in content:
      return 

    await msg.channel.send(LAUGH_TRACK_LINK)

    return

  ##############################################
  # General Cog Commands
  ##############################################

  # ADVICE COMMAND
  @commands.command( name = "advice" , aliases = ['a'] )
  async def advice( self, ctx: Context, *, question: str ) -> None:
    """
    Ask any question to the bot
    """
    await self.bot.wait_until_ready()
    
    # Create embed for sending the question
    embed = discord.Embed(
      title="**My Answer:**",
      description=
      f"{ answers [ random.randint( 0, len(answers ) ) ] }",
      color=0x42F56C )
    embed.set_footer(
      text=f"Question: { question }" )
    # Send question
    await ctx.send( embed=embed )

    return

  # HELP COMMAND
  @commands.command( name = "help", aliases = ["h"] )
  async def help( self, ctx: Context ) -> None:
    """
    Sends a link to the documentation of the bot
    """
    await self.bot.wait_until_ready()

    await ctx.send("Looks like you need some help getting around. Take a look at this link for how to use my powers to your benefit.")
    await ctx.send( HELP_LINK )

    return

  # PING COMMAND
  @commands.command( name = "ping" )
  async def ping( self, ctx: Context) -> None:
    """
    Diagnostic command to check latency on Bot Commands
    """
    await self.bot.wait_until_ready()

    await ctx.send( "Pong! The crows took {0}ms in reaching you...".format(
    round( self.bot.latency * 1000, 1 ) ) )

    return

  # STATS COMMAND
  @commands.command( name = "stats" )
  async def stats( self, ctx: Context ) -> None:
    """
      Diagnostic command to check version of python and discord.py
    """
    await self.bot.wait_until_ready()

    pythonVersion = sys.version
    dpyVersion = discord.__version__
    await ctx.send( f"I'm running on Python {pythonVersion} and discord.py {dpyVersion}! Whatever that means." )

    return

##############################################
# Setup Command for Bot
##############################################
def setup( bot : Bot ) -> None:
  logging = ConsoleLog()
  logging.send( MODULE, f"Attempting load of '{MODULE}' extension...")
  bot.add_cog( General( bot ) )

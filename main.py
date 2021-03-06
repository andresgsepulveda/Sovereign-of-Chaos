##############################################
# Package Imports
##############################################

import discord
import discord.ext
import os
import sys
sys.path.insert(1, './cogs/support')

from discord import Guild, Message
from discord_components import DiscordComponents, ComponentsBot, Button
from discord.ext import commands
from discord.ext.commands import Context

import database
from log import ConsoleLog
from timer import Timer

##############################################
# Constants and Setup
##############################################
MODULE = "MAIN"

# Initialize Bot with cmd prefix
bot = commands.Bot( 
  command_prefix = '!',
  owner = os.environ.get("OWNER_ID"))
bot.remove_command( 'help' )
DiscordComponents(bot)

DB_SETUP_PATH = "scripts/travelerdb-setup.sql"

loadTimer = Timer()
loadTimer.start()

# Connect to MySQL DB
db = database.DB()
db.start()
db.executeScriptFromFile(DB_SETUP_PATH)
db.stop()

logging = ConsoleLog()

logging.printSpacer()
logging.send( MODULE, "Starting up the bot!")

# Import Cogs from /cogs directory

logging.printSpacer()
logging.send(MODULE, 
  "Attempting load of extensions in '/cogs' directory..." )
logging.printSpacer()
if __name__ == "__main__":
  extCount = 0
  for file in os.listdir( "./cogs" ):
    if file.endswith( ".py" ):
      extension = file[:-3]
      logging.send( MODULE, f"> {extension} ")
      extCount += 1 

logging.send( MODULE , f"{extCount} extensions found in '/cogs'. Now loading...")
logging.printSpacer()

allExtensionsLoaded = True
if __name__ == "__main__":
  for file in os.listdir( "./cogs" ):
    if file.endswith( ".py" ):
      extension = file[:-3]
      # Attempt to load extension 
      # Some python files might not have a properly
      # configured setup() method, need to account for that.
      try:
        bot.load_extension( f"cogs.{extension}" )
        logging.send( MODULE, f"Loaded extension '{extension}'" )
      except Exception as e:
        exception = f"{type(e).__name__}: {e}"
        logging.send( MODULE, f"Failed to load extension {extension}\n{exception}" )
        allExtensionsLoaded = False 
      logging.printSpacer()

# Display success / failure on console
if allExtensionsLoaded:
  logging.send( MODULE, "SUCCESS: All extensions in '/cogs' directory loaded successfully!" )
else:
  logging.send( MODULE, "WARNING: One or more extensions could not be loaded. See above for error output." )

logging.printSpacer()

timeStr = loadTimer.stop()
logging.send( MODULE, f"LOAD TIME: {timeStr} seconds" )

logging.printSpacer()

##############################################
# Events
##############################################

@bot.event
async def on_guild_join( guild: Guild ) -> None:

  guildID = str(guild.id)

  return

@bot.event 
async def on_message( message: Message ) -> None:
  """
  Defines behavior for bot on receiving message in chat
  """
  # Ignore messages from self or other bots
  if message.author == bot.user or message.author.bot:
    return
  await bot.process_commands(message)
  return

@bot.event
async def on_ready():
  """
  Defines behavior for bot when ready to execute commands
  """
  # Change status on Discord
  await bot.change_presence(
    activity = discord.Activity(
      type = discord.ActivityType.watching,
      name = 'the sands of time... | !s help' ) )
  # Console output for debugging
  logging.printSpacer()
  logging.send( MODULE, "Logged in as" )
  logging.send( MODULE, bot.user.name )
  logging.send( MODULE, bot.user.id )
  logging.printSpacer()
  return

@bot.event
async def on_command_completion( ctx: Context ) -> None:
  """
  Defines behavior for bot whenever a command is completed successfully
  """
  # Console output to note whenever the bot successfully
  # runs a command
  fullCommandName = ctx.command.qualified_name
  split = fullCommandName.split( " " )
  executedCommand = str(split[0])
  logging.send( MODULE, 
    f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})" )
  return

  
##############################################
# Bot / Server Initialization
##############################################

# Runs the bot for use on Discord
bot.run(os.environ.get("SOC_DISCORD_TOKEN"))

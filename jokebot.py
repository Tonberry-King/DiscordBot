import discord
from dnspiration import QUOTES
import random
import joke_api
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name != 'test-grounds':
        return

    if message.content.startswith('$joke'):
        joke = joke_api.get_joke()
        print(joke)

        if joke == False:
            await message.channel.send("Couldn't get joke from API")
        else:
            await message.channel.send(joke['setup'] + '\n' + joke['punchline'])
            
    if message.content.startswith('Aemon'):
        await message.channel.send("Aemon is da coolest!")

    if "dnspiration" in message.content.lower():
        quote = random.choice(QUOTES)
        await message.channel.send(quote)



client.run(DISCORD_TOKEN)
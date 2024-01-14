import discord
import random
import asyncio
import os
from os.path import join, dirname
from dotenv import load_dotenv

class MyClient(discord.Client):
    async def on_ready(self):
        print('We have logged in as {0.user}')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith('$guess'):
            await message.channel.send('Guess a number between 1 and 10.')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()
            
            answer = random.randint(1,10)

            solved = False

            while solved == False:
                try:
                    guess = await self.wait_for('message', check=is_correct, timeout=5.0)
                except asyncio.TimeoutError:
                    return await message.channel.send(f'Sorry, you took too long to respond. It was {answer}.')
                
                if int(guess.content) == answer:
                    solved = True
                    await message.channel.send('You are correct!')

                elif int(guess.content) > answer:
                    await message.channel.send('Try lower...')

                elif int(guess.content) < answer: 
                    await message.channel.send('Try higher...')
                
                else:
                    await message.channel.send('Between 1 and 10?')

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
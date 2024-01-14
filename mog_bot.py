import discord
from discord.ext import commands
import random
import asyncio
import os
from os.path import join, dirname
from dotenv import load_dotenv
from cat_api import get_cat

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as: {client.user}. \n Bot is ready.")

@client.command(aliases=['hang'])
async def hangman(ctx):
    '''
    Plays Hangman.
    '''
    words= ["aemon", "lochlan", "eric", "mommy", "tunabird", "move", "sneeze"]

    word = random.choice(words)
    correct_letters = []
    incorrect_letters = []
    chances = 6
    word_state = ["-"] * len(word)

    display = await ctx.send(f"Word: {' '.join(word_state)}\nChances: {chances}")
    message = await ctx.send("---------------")
    
    game_over = False
    while not game_over:

        guess = await client.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)

        if len(guess.content) == 1 and guess.content.isalpha():
            guess.content = guess.content.lower()
            
            if guess.content in correct_letters or guess.content in incorrect_letters:
                temp = await ctx.send(f"You already guessed the letter {guess.content}. Try a different letter!")
                await asyncio.sleep(2)
                await guess.delete()
                await temp.delete()
                await display.edit(content=f"Word: {' '.join(word_state)}\nChances: {chances}")
               
            elif guess.content in word:
                correct_letters.append(guess.content)
                
                for i, c in enumerate(word):
                    if c == guess.content:
                        word_state[i] = c

                if all(c in correct_letters for c in word):
                    await guess.delete()
                    await ctx.send(f"Congratulations, you won!\nThe word was {word}")
                    game_over = True

                else:
                    temp = await ctx.send("Correct!")
                    await asyncio.sleep(1)
                    await guess.delete()
                    await temp.delete()
                    await display.edit(content=f"Word: {' '.join(word_state)}\nChances: {chances}")
            else:
                incorrect_letters.append(guess.content)
                chances -= 1
                    
                if chances == 0:
                    msg = await ctx.send(f"Incorrect!")
                    await guess.delete()
                    await asyncio.sleep(0.5)
                    await msg.delete()
                    await message.edit(content="   ------- \n"
                                            "  |     | \n"
                                            "  |     |\n"
                                            "  |     | \n"
                                            "  |     O \n"
                                            "  |    /|\ \n"
                                            "  |    / \ \n"
                                            "-----\n"
                                            "-----------------------\n"
                                            "Wrong guess. You dead!!!!\n"
                                            f"The word was {word.capitalize()}")
                    await display.edit(content=f"Word: {' '.join(word_state)}\nChances: {chances}")
                    game_over = True

                elif chances == 5:
                    msg = await ctx.send(f"Incorrect!")
                    await guess.delete()
                    await asyncio.sleep(0.5)
                    await msg.delete()
                    await message.edit(content="   -------\n"
                                                "  |\n"
                                                "  |\n"
                                                "  |\n"
                                                "  |\n"
                                                "  |\n"
                                                "  |\n"
                                                "-----\n"
                                                "-----------------------\n"
                                                "Plenty of rope left...\n")
                    await display.edit(content=f"Word: {' '.join(word_state)}\nChances: {chances}")

                elif chances == 4:
                    msg = await ctx.send(f"Incorrect!")
                    await guess.delete()
                    await asyncio.sleep(0.5)
                    await msg.delete()
                    await message.edit(content="   -------\n"
                                            "  |     | \n"
                                            "  |     |\n"
                                            "  |\n"
                                            "  |\n"
                                            "  |\n"
                                            "  |\n"
                                            "-----\n"
                                            "-----------------------\n"
                                            "Some rope left. Not great, not terrible..\n")
                    await display.edit(content=f"Word: {' '.join(word_state)}\nChances: {chances}")

                elif chances == 3:
                    msg = await ctx.send(f"Incorrect!")
                    await guess.delete()
                    await asyncio.sleep(0.5)
                    await msg.delete()
                    await message.edit(content="   -------\n"
                                            "  |     | \n"
                                            "  |     |\n"
                                            "  |     | \n"
                                            "  |\n"
                                            "  |\n"
                                            "  |\n"
                                            "-----\n"
                                            "-----------------------\n"
                                            "Uhhh... A little help?\n")
                    await display.edit(content=f"Word: {' '.join(word_state)}\nChances: {chances}")

                elif chances == 2:
                    msg = await ctx.send(f"Incorrect!")
                    await guess.delete()
                    await asyncio.sleep(0.5)
                    await msg.delete()
                    await message.edit(content="   -------\n"
                                            "  |     | \n"
                                            "  |     |\n"
                                            "  |     | \n"
                                            "  |     O \n"
                                            "  |\n"
                                            "  |\n"
                                            "-----\n"
                                            "-----------------------\n"
                                            "First time?\n")
                    await display.edit(content=f"Word: {' '.join(word_state)}\nChances: {chances}")
                    
                elif chances == 1:
                    msg = await ctx.send(f"Incorrect!")
                    await guess.delete()
                    await asyncio.sleep(0.5)
                    await msg.delete()
                    await message.edit(content="   ------- \n"
                                            "  |     | \n"
                                            "  |     |\n"
                                            "  |     | \n"
                                            "  |     O \n"
                                            "  |    /|\ \n"
                                            "  |\n"
                                            "-----\n"
                                            "-----------------------\n"
                                            "Iiiii am a maaaaan of constant sorrow....\n")
                    await display.edit(content=f"Word: {' '.join(word_state)}\nChances: {chances}")
        else:
            msg = await ctx.send("Please enter a single letter.")   
            await asyncio.sleep(0.5)   
            await guess.delete()
            await msg.delete()      

@client.command(aliases=['pong'])
async def ping(ctx):
    '''
    Get bot latency
    '''
    latency = ctx.bot.latency
    await ctx.send(latency)

@client.command()
async def echo(ctx, *, content:str):
    '''
    Echo back argument
    '''
    await ctx.send(content)

@client.command()
async def cat(ctx):
    CAT_API_TOKEN = os.environ.get('CAT_API_TOKEN')
    response = get_cat(CAT_API_TOKEN)
    url = response[0]['url']
    details = response[0]['breeds'][0]
    await ctx.send(details['name'])
    await ctx.send(url)
    await ctx.send(f"{details['description']}\nFind more information on wikipedia:\n{details['wikipedia_url']}")




DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
client.run(DISCORD_TOKEN)


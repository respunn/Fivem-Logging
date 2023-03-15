from random import *
import asyncio
import requests
import discord
from discord import app_commands
from discord.ext import commands
#from discord.utils import get
import math
#import datetime
import calendar
import time

#You need to create ".env" file for secure your token then import it.
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='!', intents= discord.Intents.all())
bot.remove_command('help')

#You need to add your server ip thingy.
serverurl = "http://server-ip:port/players.json"

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))
    try:
        sycned = await bot.tree.sync()
        print(f'Sycned {len(sycned)} global commands.')
    except Exception as e:
        print(e)


#This is for playercount, it's keep updating itself every second so you can see who joined or left the server without having server panel.
async def playercount(ctx):
    countfor = 0
    old_list = []
    check = True
    embedok=discord.Embed(title="Click to go to the file.", url=serverurl ,color=discord.Color.from_rgb(0,255,0))
    embednotok=discord.Embed(title="Click to go to the file.", url=serverurl ,color=discord.Color.from_rgb(255,0,0))
    embedok.set_author(name="JSON file reached, logging.")
    embednotok.set_author(name="Unable to reach JSON file, stopping log.")
    try:
        response = requests.get(serverurl).json()
        await ctx.send(embed=embedok)
    except requests.exceptions.RequestException as e:
        print(e)
        await ctx.send(embed=embednotok)
        check = False
    while check == True:
        current_GMT = time.gmtime()
        ts = calendar.timegm(current_GMT)
        try:
            response = requests.get(serverurl).json()
        except:
            await ctx.send(embed=embednotok)
            break
        #Once you've run it, it doesn't need to run. That's why a variable called countfor is checked.
        if countfor == 0:
            for player in response:
                #If you want to seperate some player from others and count them you can use this.
                if "steam:123456789123456" in player['identifiers']:
                    old_list.append("SeperatedPlayer")
                else:
                    old_list.append(f"{player['name']}")
            countfor = 1
        else:
            new_list = []
            for player in response:
                if "steam:123456789123456" in player['identifiers']:
                    new_list.append("SeperatedPlayer")
                else:
                    new_list.append(f"{player['name']}")
            old_set = set(old_list)
            new_set = set(new_list)
            deleted_players = old_set - new_set
            added_players = new_set - old_set
            for player in deleted_players:
                embed=discord.Embed(color=discord.Color.from_rgb(255,0,0))
                embed.add_field(name=f"{player} left the server.", value=f"<t:{ts}:F>", inline=False)
                await ctx.send(embed=embed)
            for player in added_players:
                embed=discord.Embed(color=discord.Color.from_rgb(0,255,0))
                embed.add_field(name=f"{player} joined the server.", value=f"<t:{ts}:F>", inline=False)
                await ctx.send(embed=embed)
            old_list = new_list 
        await asyncio.sleep(1)

@bot.command()
async def g(ctx):
    #Using the !g command on a channel you want allows you to logging.
    bot.loop.create_task(playercount(ctx))

#!p command that shows how many players there are.
@bot.command()
async def p(ctx):
    response = requests.get(serverurl).json()
    total_players = len(response)
    playername = ""
    #If you want to check is there any admins, you can use their discord id with it.
    Admindcidlist = [
        "123456789123456789",
        "123456789123456789"
    ]
    #If you want to check is there any potential pd players, you can use their discord id with it.
    PDdcidlist = [
        "123456789123456789",
        "123456789123456789"
    ]
    admincount = 0
    potentialpdcount = 0
    discord_id = None
    embed=discord.Embed(title="X Server's Playerlist'", color=discord.Color.from_rgb(255,255,255))
    for player in response:
        identifier = player['identifiers']
        if "steam:123456789123456" in identifier:
            playername = "Admin Name"
            admincount += 1
        else:
            playername = player['name']
        
        for identifier in player['identifiers']:
            if identifier.startswith('discord:'):
                discord_id = identifier[8:]
                if discord_id in PDdcidlist:
                    if discord_id in Admindcidlist:
                        embed.add_field(name=f"{playername} - #{player['id']}", value=f"<@{discord_id}>\nᴘᴏᴛᴇɴᴛɪᴀʟ ᴘᴅ ᴘʟᴀʏᴇʀ", inline=True)
                        potentialpdcount += 1
                    else:
                        embed.add_field(name=f"{playername} - #{player['id']}", value=f"<@{discord_id}>\nᴘᴏᴛᴇɴᴛɪᴀʟ ᴘᴅ ᴘʟᴀʏᴇʀ", inline=True)
                        potentialpdcount += 1
                else:
                    if discord_id in Admindcidlist:
                        embed.add_field(name=f"{playername} - #{player['id']}", value=f"<@{discord_id}>", inline=True)
                    else:
                        embed.add_field(name=f"{playername} - #{player['id']}", value=f"<@{discord_id}>", inline=True)

    #This is for alignment.
    if total_players%3 > .5:
        embed.add_field(name="", value="", inline=True)
    embed.set_footer(text=f"Total players: {str(total_players)}   |   Potential PD count: {str(potentialpdcount)}   |   There are {str(admincount)} admins on the server!")
    await ctx.send(embed=embed)

#You can check the resources with the !s command.
@bot.command()
async def s(ctx):
    counter = 0
    check_script_list = []
    script_list = []
    added_scripts_string = ""
    deleted_scripts_string = ""
    response = requests.get(serverurl).json()
    #You can save resources to txt file to check another time or even after restart the bot.
    with open('resourceslog.txt', 'r') as file:
        for line in file.readlines():
            check_script_list.append(line.strip())
    for resource in response['resources']:
            script_list.append(resource)
            script_list.sort()
            counter += 1
    script_list.sort()
    deleted_scripts = list(set(check_script_list) - set(script_list))
    added_scripts = list(set(script_list) - set(check_script_list))
    if len(added_scripts) != 0:
        i = 0
        while i < len(added_scripts):
            added_scripts_string += f"{added_scripts[i]}\n"
            i += 1
    if len(deleted_scripts) != 0:
        i = 0
        while i < len(deleted_scripts):
            deleted_scripts_string += f"{deleted_scripts[i]}\n"
            i += 1      
    if len(added_scripts) != 0 or len(deleted_scripts) != 0:
        open("resourceslog.txt", "w").close()
        file = open("resourceslog.txt", "w")
        i = 0
        while i < len(script_list):
            file.write(f"{script_list[i]}\n")
            i += 1
        file.close()
        await ctx.send(f"Added script(s):\n{added_scripts_string}\nDeleted script(s):\n{deleted_scripts_string}\nTotal number of script(s): {len(script_list)}")
    else:
        await ctx.send(f"There are no scripts added or deleted.\nTotal number of script(s): {len(check_script_list)}")

#In addition, the !clear command works with purge.
@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)

#You can add character names here, works with discord id.
def CharacterNames(character):
    if character.id == 123456789123456789:
        name = "Player 1"
    if character.id == 123456789123456789:
        name = "Player 2"
    return name

def saveCounter(counter):
    open("counter.txt", "w").close()
    file = open('counter.txt','w')
    file.write(counter)
    file.close()
    return

def checkCounter():
    file = open('counter.txt', 'r')
    counter = file.readline()
    counter2 = int(counter)
    file.close()
    return counter2

#Race
@bot.tree.command(name='race', description="Race standings.")
@app_commands.choices(route = [
    #You can add more race routes here, just copy paste it.
    discord.app_commands.Choice(name='Race 1', value='Race 1'),
    discord.app_commands.Choice(name="Race 2", value="Race 2")])
async def race(interaction: discord.Interaction, route: discord.app_commands.Choice[str], number_of_racers: int, entrance_fee: int, firstplace: discord.Member, secondplace: discord.Member, thirdplace: discord.Member):
    if number_of_racers < 3:
        await interaction.response.send_message(f"Numbers of racers can not be below 4.")
    else: 
        #All the code below is math, I knew how I did it at the time but I don't know now.
        total_money = int(entrance_fee * number_of_racers)
        if total_money > 34:
            firstplacemoney = total_money * .6
            secondplacemoney = total_money * .3
            thirdplacemoney = total_money * .1
            if thirdplacemoney < entrance_fee:
                total_money2 = total_money - entrance_fee
                thirdplacemoney = entrance_fee
                
                if total_money2 % 3 == 0:
                    firstplacemoney = int(total_money2 / 3 * 2)
                    secondplacemoney = int(total_money2 / 3) 
                else:
                    firstplacemoney = total_money2 * .66
                    secondplacemoney = total_money2 * .33
                    
                    firstplacemoney = round(firstplacemoney,2)
                    secondplacemoney = round(secondplacemoney,2)
                    
                    firstplacemoney2 = firstplacemoney % 1
                    firstplacemoney -= firstplacemoney2
     
                    secondplacemoney2 = secondplacemoney % 1
                    secondplacemoney -= secondplacemoney2
                    
                    total = firstplacemoney2 + secondplacemoney2
                    total = round(total)
                    
                    if total % 2 == 0:
                        firstplacemoney = int(math.floor(firstplacemoney) + total / 2)
                        secondplacemoney = int(math.floor(secondplacemoney) + total / 2)
                    elif total == 1:
                        firstplacemoney = int(math.floor(firstplacemoney) + total)
                        secondplacemoney = int(math.floor(secondplacemoney))
                    else:
                        firstplacemoney = int(math.floor(firstplacemoney) + total / 3 * 2)
                        secondplacemoney = int(math.floor(secondplacemoney) + total / 3)
            else:
                firstplacemoney = round(firstplacemoney,2)
                secondplacemoney = round(secondplacemoney,2)
                thirdplacemoney = round(thirdplacemoney,2)

                firstplacemoney2 = firstplacemoney % 1
                firstplacemoney -= firstplacemoney2
            
                secondplacemoney2 = secondplacemoney % 1
                secondplacemoney -= secondplacemoney2
            
                thirdplacemoney2 = thirdplacemoney % 1
                thirdplacemoney -= thirdplacemoney2

                total = firstplacemoney2 + secondplacemoney2 + thirdplacemoney2
                total = round(total)

                if total % 2 == 0:
                    firstplacemoney = int(math.floor(firstplacemoney) + total / 2)
                    secondplacemoney = int(math.floor(secondplacemoney) + total / 2)
                    thirdplacemoney = int(math.floor(thirdplacemoney))
                elif total == 1:
                    firstplacemoney = int(math.floor(firstplacemoney) + total)
                    secondplacemoney = int(math.floor(secondplacemoney))
                    thirdplacemoney = int(math.floor(thirdplacemoney))
                else:
                    firstplacemoney = int(math.floor(firstplacemoney) + total / 3 * 2)
                    secondplacemoney = int(math.floor(secondplacemoney) + total / 3)
                    thirdplacemoney = int(math.floor(thirdplacemoney))
        else:
            if entrance_fee == 3:
                firstandsecondplacemoney = int(total_money - entrance_fee)
                firstandsecondplacemoney = int(firstandsecondplacemoney / 3)
                firstplacemoney = int(firstandsecondplacemoney * 2)
                secondplacemoney = int(firstandsecondplacemoney)
                thirdplacemoney = entrance_fee
            else:
                total_money2 = total_money - entrance_fee
                thirdplacemoney = entrance_fee
                
                if total_money2 % 3 == 0:
                    firstplacemoney = int(total_money2 / 3 * 2)
                    secondplacemoney = int(total_money2 / 3) 
                else:
                    firstplacemoney = total_money2 * .66
                    secondplacemoney = total_money2 * .33
                    
                    firstplacemoney = round(firstplacemoney,2)
                    secondplacemoney = round(secondplacemoney,2)
                    
                    firstplacemoney2 = firstplacemoney % 1
                    firstplacemoney -= firstplacemoney2
     
                    secondplacemoney2 = secondplacemoney % 1
                    secondplacemoney -= secondplacemoney2
                    
                    total = firstplacemoney2 + secondplacemoney2
                    total = round(total)
                    
                    if total % 2 == 0:
                        firstplacemoney = int(math.floor(firstplacemoney) + total / 2)
                        secondplacemoney = int(math.floor(secondplacemoney) + total / 2)
                    elif total == 1:
                        firstplacemoney = int(math.floor(firstplacemoney) + total)
                        secondplacemoney = int(math.floor(secondplacemoney))
                    else:
                        firstplacemoney = int(math.floor(firstplacemoney) + total / 3 * 2)
                        secondplacemoney = int(math.floor(secondplacemoney) + total / 3)
        
        counter =  checkCounter()
        firstplace = CharacterNames(firstplace)
        secondplace = CharacterNames(secondplace)
        thirdplace = CharacterNames(thirdplace)
        if firstplace == secondplace or firstplace == thirdplace or secondplace == thirdplace:
            if firstplace == secondplace and secondplace == thirdplace:
                await interaction.response.send_message(f"No person **cannot** be in two or three rows in the rankings.\nYou wrote **{secondplace}** in both the first, the second and the third.")
            elif firstplace == secondplace:
                await interaction.response.send_message(f"No person **cannot** be in two or three rows in the rankings.\nYou wrote **{firstplace}** in both the first and the second.")
            elif firstplace == thirdplace:
                await interaction.response.send_message(f"No person **cannot** be in two or three rows in the rankings.\nYou wrote **{firstplace}** in both the first and the third.")
            elif secondplace == thirdplace:
                await interaction.response.send_message(f"No person **cannot** be in two or three rows in the rankings.\nYou wrote **{secondplace}** in both the second and the third.")
        else:
            await interaction.response.send_message(f"**Race #{counter} {route.name}**\nTotal: {total_money} Black Coin\n\nTop 3 out of {number_of_racers} racers:\n**1.** {firstplace} - {firstplacemoney} Black Coin\n**2.** {secondplace} - {secondplacemoney} Black Coin\n**3.** {thirdplace} - {thirdplacemoney} Black Coin")
            saveCounter(str(counter + 1))

#It does what it writes.
@bot.tree.command(name='changecounter', description="Changing the counter.")
@app_commands.checks.has_permissions(administrator=True)
async def changecounter(interaction: discord.Interaction, new_counter: int):
    try:
        saveCounter(str(new_counter))
        await interaction.response.send_message(f"Successfully changed the counter to **{new_counter}**.")
    except:
        await interaction.response.send_message(f"Changing the counter failed.", ephemeral=True)

#It does what it writes.
@bot.tree.command(name='checkcounter', description="Checking the counter.")
@app_commands.checks.has_permissions(administrator=True)
async def checkcounter(interaction: discord.Interaction):
    try:
        counter = checkCounter()
        await interaction.response.send_message(f"The current counter is **{counter}**.")
    except:
        await interaction.response.send_message(f"Command failed.", ephemeral=True)


bot.run(TOKEN)

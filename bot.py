from random import *
import asyncio
import requests
import discord
from discord import app_commands
from discord.ext import commands
import math
import calendar
import time


#You need to create ".env" file for secure your token then import it.
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")


#Assigning bot.
bot = commands.Bot(command_prefix='!', intents= discord.Intents.all())
bot.remove_command('help')


#You need to add your server ip and port.
server_ip = "play.server.net"
port = "30120"
serverurl = f"http://{server_ip}:{port}/players.json" #YOU DON'T NEED TO TOUCH THIS.


#To get a reaction and enter details when the bot is ready.
@bot.event
async def on_ready():
    #Setting status.
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
    #Printing bot's details.
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))
    try:
        #Trying to sync commands.
        sycned = await bot.tree.sync()
        print(f'Sycned {len(sycned)} global commands.')
    except Exception as e:
        print(e)


#This is for playercount, it's keep updating itself every second so you can see who joined or left the server without having server panel.
async def playercount(ctx):
    #We have to run it once and save the data or it goes into the loop.
    did_it_work_check = True
    request_check = True
    
    #We need to create old_list outside of loop.
    old_list = []
    
    #Creating embeds.
    embedok=discord.Embed(title="Click to go to the file.", url=serverurl ,color=discord.Color.from_rgb(0,255,0))
    embednotok=discord.Embed(title="Click to go to the file.", url=serverurl ,color=discord.Color.from_rgb(255,0,0))
    embedok.set_author(name="JSON file reached, logging.")
    embednotok.set_author(name="Unable to reach JSON file, stopping log.")
    
    #Trying to access JSON file.
    try:
        response = requests.get(serverurl).json()
        #If the JSON file can be accessed, continue the code and post embed.
        await ctx.send(embed=embedok)
    except requests.exceptions.RequestException as e:
        print(e) #Printing error.
        
        #If the JSON file cannot be accessed, break the code and post embed.
        await ctx.send(embed=embednotok)
        request_check = False #Using variable here to check is there any issue for going inside of a loop.
    
    while request_check == True:
        #Assinging time every loop.
        current_GMT = time.gmtime()
        ts = calendar.timegm(current_GMT)
        
        #Trying to access JSON file every loop.
        try:
            response = requests.get(serverurl).json()
        except:
            await ctx.send(embed=embednotok)
            #If the JSON file cannot be accessed, break the code and post embed.
            break
        
        if did_it_work_check == True:
            #Appending players to new_list.
            for player in response:
                #If you want to seperate some player from others and count them you can use this.
                if "steam:123456789123456" in player['identifiers']:
                    old_list.append("SeperatedPlayer")
                else:
                    old_list.append(f"{player['name']}")
            did_it_work_check = False
        else:
            #Creating new_list for to compare old_list.
            new_list = []
            
            #Appending players to new_list.
            for player in response:
                #If you want to seperate some player from others and count them you can use this.
                if "steam:123456789123456" in player['identifiers']:
                    new_list.append("SeperatedPlayer")
                else:
                    new_list.append(f"{player['name']}")
            
            #Compare lists and assigning to new lists.
            old_set = set(old_list)
            new_set = set(new_list)
            deleted_players = old_set - new_set
            added_players = new_set - old_set
            
            #Adding data to embed.
            for player in deleted_players:
                embed=discord.Embed(color=discord.Color.from_rgb(255,0,0))
                embed.add_field(name=f"{player} left the server.", value=f"<t:{ts}:F>", inline=False)
                await ctx.send(embed=embed)
            
            for player in added_players:
                embed=discord.Embed(color=discord.Color.from_rgb(0,255,0))
                embed.add_field(name=f"{player} joined the server.", value=f"<t:{ts}:F>", inline=False)
                await ctx.send(embed=embed)
            
            #After adding datas to embed, assign the new list to the old list.
            old_list = new_list
        
        #Waiting 1 second for new loop.
        await asyncio.sleep(1)


#Using the !g command on a channel you want allows you to logging.
@bot.command()
async def g(ctx):
    bot.loop.create_task(playercount(ctx))


#!p command that shows how many players there are.
@bot.command()
async def p(ctx):
    try:
        #Trying to access json file.
        response = requests.get(serverurl).json()
        total_players = len(response)
        #If you want to check is there any admins, you can use their discord id with it.
        adminDCidentifier = [
            "123456789123456789",
            "123456789123456789"
        ]
        admincount = 0
        potentialpdcount = 0
        discord_id = None
        embed=discord.Embed(title="X Server's Playerlist'", color=discord.Color.from_rgb(255,255,255))
        for player in response:
            #Getting player name.
            identifier = player['identifiers']
            if "steam:123456789123456" in identifier:
                playername = "Admin Name"
                admincount += 1
            else:
                playername = player['name']
            
            #After getting player name, adding discord mention and in game id to embed.
            for identifier in player['identifiers']:
                if identifier.startswith('discord:'):
                    discord_id = identifier[8:]
                    if discord_id in adminDCidentifier:
                        embed.add_field(name=f"{playername} - #{player['id']}", value=f"<@{discord_id}>", inline=True)
                    else:
                        embed.add_field(name=f"{playername} - #{player['id']}", value=f"<@{discord_id}>", inline=True)
                            
        #This is for alignment.
        if total_players%3 > .5:
            embed.add_field(name="", value="", inline=True)
        
        #Adding datas to footer and printing it to discord.
        embed.set_footer(text=f"Total players: {str(total_players)}   |   Potential PD count: {str(potentialpdcount)}   |   There are {str(admincount)} admins on the server!")
        await ctx.send(embed=embed)
        
    except requests.exceptions.RequestException as e:
        print(e) #Printing error.


#You can check the resources with the !s command.
@bot.command()
async def s(ctx):
    #Assigning variables.
    counter = 0
    script_list = []
    check_script_list = []
    added_scripts_string = ""
    deleted_scripts_string = ""
    
    try:
        #Trying to access json file.
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
        
        #Compare lists and assigning to new lists.
        deleted_scripts = list(set(check_script_list) - set(script_list))
        added_scripts = list(set(script_list) - set(check_script_list))
        
        #Assigning data to strings.
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
                
        #If there is no deleted or added script, we first clean the txt file and then save the new data.
        if len(added_scripts) != 0 or len(deleted_scripts) != 0:
            open("resourceslog.txt", "w").close()
            file = open("resourceslog.txt", "w")
            i = 0
            while i < len(script_list):
                file.write(f"{script_list[i]}\n")
                i += 1
            file.close()
            
            #Sending message to discord.
            await ctx.send(f"Added script(s):\n{added_scripts_string}\nDeleted script(s):\n{deleted_scripts_string}\nTotal number of script(s): {len(script_list)}")
        else:
            await ctx.send(f"There are no scripts added or deleted.\nTotal number of script(s): {len(check_script_list)}")
            
    except requests.exceptions.RequestException as e:
        print(e) #Printing error.


#In addition, the !clear command works with purge.
@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)


#You can set character names to discord mentions.
def CharacterNames(character):
    if character.id == 123456789123456789:
        name = "Player 1"
    if character.id == 123456789123456789:
        name = "Player 2"
    return name


#Race command.
@bot.tree.command(name='race', description="Race standings.")
@app_commands.choices(route = [
    #You can add more race routes here, just copy paste it.
    discord.app_commands.Choice(name='Race 1', value='Race 1'),
    discord.app_commands.Choice(name="Race 2", value="Race 2")
    ])
async def race(interaction: discord.Interaction, route: discord.app_commands.Choice[str], number_of_racers: int, entrance_fee: int, firstplace: discord.Member, secondplace: discord.Member, thirdplace: discord.Member):
    #Checking number of racers.
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
        
        #Assigning data to variables.
        counter =  checkCounter()
        firstplace = CharacterNames(firstplace)
        secondplace = CharacterNames(secondplace)
        thirdplace = CharacterNames(thirdplace)
        
        #To prevent the same people from being in a different order.
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
            #Sending message to discord.
            await interaction.response.send_message(f"**Race #{counter} {route.name}**\nTotal: {total_money} Black Coin\n\nTop 3 out of {number_of_racers} racers:\n**1.** {firstplace} - {firstplacemoney} Black Coin\n**2.** {secondplace} - {secondplacemoney} Black Coin\n**3.** {thirdplace} - {thirdplacemoney} Black Coin")
            #Saving race count.
            saveCounter(str(counter + 1))


#Saving counter from discord.
def saveCounter(counter):
    open("counter.txt", "w").close()
    file = open('counter.txt','w')
    file.write(counter)
    file.close()
    return

#It does what it writes.
@bot.tree.command(name='changecounter', description="Changing the counter.")
@app_commands.checks.has_permissions(administrator=True)
async def changecounter(interaction: discord.Interaction, new_counter: int):
    try:
        saveCounter(str(new_counter))
        await interaction.response.send_message(f"Successfully changed the counter to **{new_counter}**.")
    except:
        await interaction.response.send_message(f"Changing the counter failed.", ephemeral=True)


#Checking counter from discord.
def checkCounter():
    file = open('counter.txt', 'r')
    counter = file.readline()
    counter2 = int(counter)
    file.close()
    return counter2

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
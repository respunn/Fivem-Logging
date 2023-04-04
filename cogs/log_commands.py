# Importing modules from separate file
from important_files.imports import *

# Importing config values from separate file
from important_files.config import *
# If you want to check is there any admins, you can use their discord id with it.
from players.log_admin_ids import *

class log_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self, ctx):
        print('Log commands cog is ready.')
        
        print('Logging has started.')
        did_it_work_check = True
        request_check = True
        
        # We need to create old_list outside of loop.
        old_list = []
        
        # Creating embeds.
        embedok=discord.Embed(title="Click to go to the file.", url=serverurl ,color=discord.Color.from_rgb(0,255,0))
        embednotok=discord.Embed(title="Click to go to the file.", url=serverurl ,color=discord.Color.from_rgb(255,0,0))
        embedok.set_author(name="JSON file reached, logging.")
        embednotok.set_author(name="Unable to reach JSON file, stopping log.")
        
        # Trying to access JSON file.
        try:
            response = requests.get(serverurl).json()
            # If the JSON file can be accessed, continue the code and post embed.
            await ctx.send(embed=embedok)
        except requests.exceptions.RequestException as e:
            print(e) # Printing error.
            
            # If the JSON file cannot be accessed, break the code and post embed.
            await ctx.send(embed=embednotok)
            request_check = False # Using variable here to check is there any issue for going inside of a loop.
        
        while request_check == True:
            # Assinging time every loop.
            current_GMT = time.gmtime()
            ts = calendar.timegm(current_GMT)
            
            # Trying to access JSON file every loop.
            try:
                response = requests.get(serverurl).json()
            except:
                await ctx.send(embed=embednotok)
                # If the JSON file cannot be accessed, break the code and post embed.
                break
            
            if did_it_work_check == True:
                # Appending players to new_list.
                for player in response:
                    # If you want to seperate some player from others and count them you can use this.
                    if "steam:123456789123456" in player['identifiers']:
                        old_list.append("SeperatedPlayer")
                    else:
                        old_list.append(f"{player['name']}")
                did_it_work_check = False
            else:
                # Creating new_list for to compare old_list.
                new_list = []
                
                # Appending players to new_list.
                for player in response:
                    #If you want to seperate some player from others and count them you can use this.
                    if "steam:123456789123456" in player['identifiers']:
                        new_list.append("SeperatedPlayer")
                    else:
                        new_list.append(f"{player['name']}")
                
                # Compare lists and assigning to new lists.
                old_set = set(old_list)
                new_set = set(new_list)
                deleted_players = old_set - new_set
                added_players = new_set - old_set
                
                # Adding data to embed.
                for player in deleted_players:
                    embed=discord.Embed(color=discord.Color.from_rgb(255,0,0))
                    embed.add_field(name=f"{player} left the server.", value=f"<t:{ts}:F>", inline=False)
                    await ctx.send(embed=embed)
                
                for player in added_players:
                    embed=discord.Embed(color=discord.Color.from_rgb(0,255,0))
                    embed.add_field(name=f"{player} joined the server.", value=f"<t:{ts}:F>", inline=False)
                    await ctx.send(embed=embed)
                
                # After adding datas to embed, assign the new list to the old list.
                old_list = new_list
            
            # Waiting 1 second for new loop.
            await asyncio.sleep(1)
    
    # !p command that shows how many players there are.
    @commands.command()
    async def p(ctx):
        try:
            # Trying to access json file.
            response = requests.get(serverurl).json()
            total_players = len(response)
            
            admincount = 0
            potentialpdcount = 0
            discord_id = None
            embed=discord.Embed(title="X Server's Playerlist'", color=discord.Color.from_rgb(255,255,255))
            for player in response:
                # Getting player name.
                identifier = player['identifiers']
                
                # You can add custom names to specific discord ids.
                if "steam:123456789123456" in identifier:
                    playername = "Admin Name"
                    admincount += 1
                else:
                    playername = player['name']
                
                #After getting player name, adding discord mention and in game id to embed.
                for identifier in player['identifiers']:
                    if identifier.startswith('discord:'):
                        discord_id = identifier[8:]
                        if discord_id in admins_discord_ids:
                            embed.add_field(name=f"{playername} - #{player['id']}", value=f"<@{discord_id}>", inline=True)
                        else:
                            embed.add_field(name=f"{playername} - #{player['id']}", value=f"<@{discord_id}>", inline=True)
            
            # This is for alignment.
            if total_players%3 > .5:
                embed.add_field(name="", value="", inline=True)
            
            # Adding datas to footer and printing it to discord.
            embed.set_footer(text=f"Total players: {str(total_players)}   |   Potential PD count: {str(potentialpdcount)}   |   There are {str(admincount)} admins on the server!")
            await ctx.send(embed=embed)
            
        except requests.exceptions.RequestException as e:
            print(e) # Printing error.

    # You can check the resources with the !s command.
    @commands.command()
    async def s(self, ctx):
        # Assigning variables.
        counter = 0
        script_list = []
        check_script_list = []
        added_scripts_string = ""
        deleted_scripts_string = ""
        
        try:
            # Trying to access json file.
            response = requests.get(serverurl).json()
            
            # You can save resources to txt file to check another time or even after restart the bot.
            with open('resourceslog.txt', 'r') as file:
                for line in file.readlines():
                    check_script_list.append(line.strip())
            for resource in response['resources']:
                    script_list.append(resource)
                    script_list.sort()
                    counter += 1
            script_list.sort()
            
            # Compare lists and assigning to new lists.
            deleted_scripts = list(set(check_script_list) - set(script_list))
            added_scripts = list(set(script_list) - set(check_script_list))
            
            # Assigning data to strings.
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
                    
            # If there is no deleted or added script, we first clean the txt file and then save the new data.
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
            print(e) # Printing error.

def setup(bot):
    bot.add_cog(log_commands(bot))
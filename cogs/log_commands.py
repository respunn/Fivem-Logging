# Importing modules from separate file
from important_files.imports import *

# Importing config values from separate file
from important_files.config import *
# If you want to check is there any admins, you can use their discord id with it.
from players.log_admin_ids import *

def connection():
        try:
            response = requests.get(serverurl).json()
            # If the JSON file can be accessed, return the data.
            return response
        except requests.exceptions.RequestException as e:
            print(e) # Printing error.
            return

class log_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_running = True
        self.last_error_time = 0
        self.is_connected = False
        self.old_list_from_outside = []
        self.did_it_work_check = True
        self.logging_players.start()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Log commands cog is ready.')
    
    @tasks.loop(seconds=1)
    async def logging_players(self):
        if self.is_running:
            channel = self.bot.get_channel(channelid)
            
            current_GMT = time.gmtime()
            ts = calendar.timegm(current_GMT)
            
            embedok=discord.Embed(title="Click to go to the file.", url=serverurl ,color=discord.Color.from_rgb(0,255,0))
            embedok.add_field(name="JSON file reached, logging.", value=f"<t:{ts}:F>", inline=False)
            embednotok=discord.Embed(title="Click to go to the file.", url=serverurl ,color=discord.Color.from_rgb(255,0,0))
            embednotok.add_field(name="Unable to reach JSON file.", value=f"<t:{ts}:F>", inline=False)
            
            # Attempt to connect to a link
            response = await connection()
            
            # Reset the old and new lists at the start of each iteration of the loop
            old_list = self.old_list_from_outside.copy()
            new_list = []
            
            # If connection fails and 60 seconds have elapsed since last error message
            if not response and time.time() - self.last_error_time >= 60:
                # Send error message
                await channel.send(embed=embednotok)
                self.last_error_time = time.time() # Update last error time
                self.is_connected = False
            else:
                if not self.is_connected:
                    # Send "JSON file reached" message only once when the connection is established
                    self.is_connected = True
                    await channel.send(embed=embedok)
                
                if self.did_it_work_check == True:
                    # Appending players to old_list first.
                    for player in response:
                        for identifier in player['identifiers']:
                            if identifier in separated:
                                # Append the name associated with the identifier to the old_list
                                old_list.append(separated[identifier])
                                break  # Skip the rest of the identifiers for this player
                            else:
                                old_list.append(f"{player['name']}")
                    self.did_it_work_check = False
                else:
                    # Appending players to new_list.
                    for player in response:
                        for identifier in player['identifiers']:
                            if identifier in separated:
                                # Append the name associated with the identifier to the new_list
                                new_list.append(separated[identifier])
                                break  # Skip the rest of the identifiers for this player
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
                        await channel.send(embed=embed)
                    
                    for player in added_players:
                        embed=discord.Embed(color=discord.Color.from_rgb(0,255,0))
                        embed.add_field(name=f"{player} joined the server.", value=f"<t:{ts}:F>", inline=False)
                        await channel.send(embed=embed)
                    
                    # After adding datas to embed, assign the new list to the old list.
                    self.old_list_from_outside = new_list.copy()
    
    @logging_players.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()
    
    @logging_players.after_loop
    async def after_my_task(self):
        channel = self.bot.get_channel(channelid)
        embed=discord.Embed(title="", color=discord.Color.from_rgb(255,0,0))
        embed.set_author(name="The log loop is broken.")
        await channel.send(embed)
    
    @commands.command()
    async def stoplog(self, ctx):
        self.is_running = False
        embed=discord.Embed(title="", color=discord.Color.from_rgb(255,165,0))
        embed.set_author(name="Logging has been stopped.")
        await ctx.send(embed)
    
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
# Importing modules from separate file
from important_files.imports import *

# Importing config values from separate file
from important_files.config import *
# If you want to check is there any admins, you can use their discord id with it.
from players.log_admin_ids import *

class log_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_error_time = 0
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Log commands cog is ready.')
    
    @tasks.loop(seconds=1)
    async def logging_players(self):
        # Attempt to connect to a link
        success = await connect_to_link()
        
        # If connection fails and 60 seconds have elapsed since last error message
        if not success and time.time() - self.last_error_time >= 60:
            # Send error message
            channel = self.bot.get_channel(1234567890) # Replace with your channel ID
            await channel.send("Failed to connect to link.")
            self.last_error_time = time.time() # Update last error time
    
    @logging_players.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()
    
    @logging_players.after_loop
    async def after_my_task(self):
        channel = self.bot.get_channel(channelid) # Replace with your channel ID
        await channel.send("The log loop is broken.")
    
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
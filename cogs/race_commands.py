# Importing modules from separate file
from important_files.imports import *

# Importing config values from separate file
from important_files.config import *
from players.racers_names import *

class race_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Race commands cog is ready.')
    
    #Saving counter from discord.
    def saveCounter(counter):
        open("counter.txt", "w").close()
        file = open('counter.txt','w')
        file.write(counter)
        file.close()
        return
    
    #Checking counter from discord.
    def checkCounter(self, interaction: discord.Interaction):
        file = open('counter.txt', 'r')
        counter = file.readline()
        counter2 = int(counter)
        file.close()
        return counter2

    #It does what it writes.
    @app_commands.command(name='checkcounter', description="Checking the counter.")
    @app_commands.checks.has_permissions(administrator=True)
    async def checkcounter(interaction: discord.Interaction):
        try:
            counter = race_commands.checkCounter()
            await interaction.response.send_message(f"The current counter is **{counter}**.")
        except:
            await interaction.response.send_message(f"Command failed.", ephemeral=True)
    
    #It does what it writes.
    @app_commands.command(name='changecounter', description="Changing the counter.")
    @app_commands.checks.has_permissions(administrator=True)
    async def changecounter(interaction: discord.Interaction, new_counter: int):
        try:
            race_commands.saveCounter(str(new_counter))
            await interaction.response.send_message(f"Successfully changed the counter to **{new_counter}**.")
        except:
            await interaction.response.send_message(f"Changing the counter failed.", ephemeral=True)

    #Race command.
    @app_commands.command(name='race', description="Race standings.")
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
            counter =  race_commands.checkCounter()
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
                race_commands.saveCounter(str(counter + 1))

def setup(bot):
    bot.add_cog(race_commands(bot))
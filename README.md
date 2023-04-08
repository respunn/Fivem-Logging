# Discord bot for logging player count, server resources and racing commands for a FiveM server

!!! I didn't test it, there is a chance that this code won't work.

This is a Python script that uses the `discord.py` and `requests` libraries to create a Discord bot that can log the player count and server resources in a game server. Bot getting datas from json files from server, if they are hidden you can't log anything from this bot. The bot is also designed to facilitate races between users within a Discord server, and includes a variety of features such as race standings, character name assignments, and a command to clear messages in a channel.

## Prerequisites

Before you can use this bot, you need to make sure you have the following:

- A Discord account and a server where you have the appropriate permissions to add a bot and create commands
- A game server with an IP address and a port number where the server resources and player count can be accessed via a JSON file
- A `.env` file where you can store your Discord bot's token in a secure way

## Installation

1. Clone this repository or download the script files to your local machine.
2. Install the required Python libraries by running the following command in your terminal: `pip install discord.py requests python-dotenv`.
3. Create a `.env` file in the same directory as your script files, and add your Discord bot token to the file in the following format: 

`TOKEN = 'your_discord_bot_token'`

5. Open the config file and update the `server_ip` and `port` variables with the IP address and port number of your game server.
6. You can add admin's discord ids to players/log_admin_ids file.
7. In your Discord server, create a new bot application and invite it to your server with the appropriate permissions.
8. Start the bot by running the script in your terminal: `python bot.py`.

## Usage

Once the bot is running, you can use the following commands in your Discord server:

- **Logging:** It will start logging immediately after running the bot, you can change which channel bot need to send messages to from config file. 
- `!playerlist`: This command will display a list of players in your game server, along with their Discord mentions and in-game IDs. You can also use this command to check the number of admins and potential PD (police department) players on the server.
- `!scriptlist`: This command will display a list of resources running on your game server, along with any new resources that have been added or deleted since the last time the command was used. The list is saved to a text file for future reference.
- `!startlog`: It does what it says. (You don't need to write this command when you activate the bot, bot will start log automatically.)
- `!stoplog`: It does what it says.
## Race (Work in Progress)

The `route` parameter determines which race is being run, and `number_of_racers` and `entrance_fee` are used to calculate the total winnings. The top three players are passed as `discord.Member` objects to the command, and their winnings are calculated and displayed in the output message. Also you can set character names to discord mentions.

- `!race [route] [number_of_racers] [entrance_fee] [firstplace] [secondplace] [thirdplace]`: Calculates the payout for a race and displays the top three finishers.
- `!changecounter [new_counter]`: Changes the race counter to a new value.
- `!checkcounter`: Displays the current value of the race counter.

These functions allow the bot to save and retrieve a counter value from a text file. This counter value is used to keep track of the race number for each race run by the bot. You can change discord members name's to whatever you want from players/racers_names file.

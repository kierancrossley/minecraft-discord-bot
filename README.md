# 👾 Minecraft Server Status Discord Bot
- This was a simple project using Python to send Minecraft server information to players on Discord
- This project used the [Discord.py](https://discordpy.readthedocs.io/en/stable/) library
- This project was created to practice with Discord.py 
## 💻 Server Query via Bot Status
- At regular intervals, the Discord bot will query the game server to obtain the number of players connected, if it is online 
- If the game server was offline, the bot status would turn to the red, do not disturb mode and its status will display as offline
- If the game server was online, the bot status would turn to the green, online mode and display the numbers of players connected
- If the game server was online, but the server was full, it would display that the server is full, and the bot status would change to the yellow, idle mode
- The bot sends a temporary message that deletes after 15 minutes in a defined channel to announce when the server has come online or gone offline 
## 💻 Server Query via Bot Command
- Members on the same server as the Discord bot could excute the status command to receive more information about the game server, which inludes:
  - Server online status
  - Player count
  - Server ping
  - Name of players connected
- If the server was offline, it would display that as the message
- Both results display the user who requested the message to be sent
## 💻 IP via Bot Command
- Sends the server ip address into the chat for the player to connect with

from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_responses

#STEP 0: Load our token from a safe source.
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
#print(TOKEN)

#STEP 1: Bot setup.
intents: Intents = Intents.default()
intents.message_content = True #NOQA
client: Client = Client(intents=intents)

#STEP 2: Message functionality
async def send_message(message: Message, user_message : str) -> None:
    if not user_message:
        print("(Message was empty because intents were not enabled probably)")
        return

    if is_private := user_message[0] == "?":
        user_message = user_message[1:]

    try:
        response: str = get_responses(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

#Steep 3: Handling the startup for out bot.
@client.event
async def on_ready() -> None:
    print(f"{client.user} has connected to Discord!")

#Step 4: Hnadling incoming messages.
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = str(message.content)
    channel : str = str(message.channel)

    print(f"{channel}, {username} says: {user_message}")
    await send_message(message, user_message)

#Step 5: Main entry point.
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()
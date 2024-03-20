import discord
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timedelta, timezone


load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL = int(os.getenv('CHANNEL_ID'))

timezoneadjust = int(1)

day1 = (11,0,2) # wednesday noon
day2 = (11,0,4) # friday noon


messageDay1 = " :robot: Hei alle sammen! :robot: \n\nGod onsdag.\nDet er på tide å gi en liten oppdatering på hva vi har gjort siden sist. Hva har du jobbet med siden sist? Hva skal du jobbe med fremover? Er det noe du trenger hjelp med? Vær kort og konsis, det holder med et par setninger. \n\nHa en fin dag videre! :smile:"



messageDay2 = " :robot: Hei alle sammen! :robot: \n\n God fredag. Stand-up bot her! \nDet er på tide å gi en liten oppdatering på hva vi har gjort siden sist. Hva har du jobbet med siden sist? Hva skal du jobbe med fremover? Er det noe du trenger hjelp med? Vær kort og konsis, og husk at dette er en fin mulighet til å dele kunnskap og erfaringer med hverandre. \n\nHa en fantastisk helg! :smile:"




# Define the intents
intents = discord.Intents.default()  # This sets up the intents obj with default values.
intents.messages = True  # We specifically enable the message intent.

client = discord.Client(intents=intents)


async def time_until_target(hour, minute, target_weekday):
    """Calculate the time until the next target weekday and time."""
    now = datetime.now(timezone.utc)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    while target.weekday() != target_weekday or target < now:
        target += timedelta(days=1) # Go to next day
    return (target - now).total_seconds()

        

async def send_weekly_message():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL)  # Replace with the actual channel ID
    if not channel:
        print("Channel not found!")
        return
    
    while not client.is_closed():
        # Schedule for the first message
        wait_seconds_1 = await time_until_target(day1[0], day1[1], day1[2])
        # Schedule for the second message
        wait_seconds_2 = await time_until_target(day2[0], day2[1], day2[2])

        # Determine the next event to wait for
        wait_seconds = min(wait_seconds_1, wait_seconds_2)
        print(f"Waiting for {wait_seconds} seconds until the next message.")
        await asyncio.sleep(wait_seconds)
        
        if channel:
            # Check which event is occurring
            if wait_seconds == wait_seconds_1:
                await channel.send(messageDay1)
            else:
                await channel.send(messageDay2)
                
            # Add a short delay to prevent immediate reevaluation in edge cases
            await asyncio.sleep(10)

        
        
        
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
    # Send an initial message when the bot starts
    initial_channel = client.get_channel(CHANNEL)  # Replace with the actual channel ID
    if initial_channel:
        await initial_channel.send('Hei, jeg kommer til å henge litt her fremover. :robot:')
    else:
        print("Initial channel not found!")
    
    # Start the task for sending weekly messages
    client.loop.create_task(send_weekly_message())


client.run(TOKEN)
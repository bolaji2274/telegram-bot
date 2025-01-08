from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

load_dotenv()

# Replace with your Telegram API credentials
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
phone_number = '+2349155113797'  # Your phone number registered with Telegram

# Initialize the client
client = TelegramClient('dice_forward_bot', API_ID, API_HASH)

async def copy_dice_to_group(dice_message_id, group_username):
    # Retrieve the dice message from your saved messages
    saved_messages = await client.get_messages('me', limit=10)  # Limit to recent messages in saved messages

    # Find the dice message using its ID
    dice_message = None
    for message in saved_messages:
        if message.id == dice_message_id:
            dice_message = message
            break

    if dice_message:
        # Send the dice message to the group chat
        await client.send_message(group_username, dice_message)

@client.on(events.NewMessage(pattern='/copydice'))
async def copy_dice(event):
    """ Trigger the dice copying when user sends '/copydice' command """
    # Here, you will manually input the dice message ID (the one with the result of 2)
    dice_message_id = 12345  # The ID of the dice message you want to copy (replace this with actual ID)
    group_username = -4671858349  # The target group where you want to send the dice

    # Copy the dice to the group
    await copy_dice_to_group(dice_message_id, group_username)

# Start the client
async def main():
    # Handle login manually by sending the phone number
    await client.start()  # Telethon will handle phone number and code

    print("Bot is running...")
    await client.run_until_disconnected()

# Run the main function
import asyncio
asyncio.run(main())

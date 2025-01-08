import sys
import pygame
import random
import time
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import os
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

load_dotenv()

# Telegram API credentials
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE_NUMBER = '+2349155113797'  # Replace with your phone number
SESSION_NAME = "dice_forward_bot"

# Function to retrieve the dice result from Telegram
def get_dice_result(client):
    try:
        messages = client.get_messages('me', limit=10)
        print("Messages fetched successfully.")
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return None

    for msg in messages:
        if msg.dice:
            return msg.dice.value
    return None

# Function to set up OpenGL with lighting
def setup_opengl():
    glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])  # Set light position
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])  # Set light color

# Function to draw the dice face (Cube) in 3D using OpenGL
def draw_dice_face():
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)  # Example color (white)
    # Cube Front Face (dice front face)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)

    # Cube Back Face
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, -1, -1)

    # Cube Top Face
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)

    # Cube Bottom Face
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)

    # Cube Right Face
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)

    # Cube Left Face
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)
    
    glEnd()

# Function to simulate a smooth rolling dice animation in 3D
def roll_dice_animation(client, result, output_file='dice_result.png'):
    pygame.init()

    # Set up screen for animation
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)  # Adjusting the camera's initial position
    setup_opengl()

    frames = 30  # Number of frames for the roll animation
    roll_results = [random.choice([1, 2, 3, 4, 5, 6]) for _ in range(frames)]

    # Loop through the frames to create the rolling effect
    start_time = time.time()
    while time.time() - start_time < 3:  # Limit the duration of the animation
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Draw each frame
        for i in range(frames):
            glRotatef(random.randint(1, 360), 1, 1, 0)  # Rotate around a random axis
            draw_dice_face()  # Draw the dice as a cube
            pygame.display.flip()
            pygame.time.wait(50)  # Adjust the speed of the animation

        # Break the loop after 3 seconds of animation
        if time.time() - start_time > 3:
            break

    # Save the final result as an image after animation
    pygame.image.save(pygame.display.get_surface(), output_file)
    pygame.quit()

    # Convert the saved image to a .webp format (necessary for Telegram stickers)
    image = Image.open(output_file)
    image = image.convert("RGBA")  # Ensure RGBA for transparency
    webp_file = output_file.replace('.png', '.webp')
    image.save(webp_file, 'WEBP')

    # Remove the original PNG file (optional)
    os.remove(output_file)

    return webp_file

# Function to send the recreated dice as a sticker to Telegram group
def send_dice_to_group(client, group_name, dice_sticker_path):
    # Send the sticker to the group using the send_file method
    client.send_file(group_name, dice_sticker_path, caption="Here is the dice roll result!")
    print(f"Dice result sent as sticker to group '{group_name}'!")

# Main function to orchestrate the process
def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    client.connect()

    if not client.is_user_authorized():
        print("Logging in...")
        client.send_code_request(PHONE_NUMBER)
        try:
            client.sign_in(PHONE_NUMBER, input("Enter the code you received: "))
        except Exception as e:
            if "SessionPasswordNeededError" in str(e):
                password = input("Enter your two-step verification password: ")
                client.sign_in(password=password)
            else:
                print(f"Unexpected error: {e}")
                sys.exit()

    # Retrieve dice result from Telegram
    dice_result = get_dice_result(client)
    if dice_result is None:
        print("No dice roll found in recent messages.")
        sys.exit()

    print(f"Extracted dice result: {dice_result}")
    dice_sticker = roll_dice_animation(client, dice_result)  # Create the animated dice roll and convert to .webp

    target_group = -4671858349  # Replace with your group username or ID
    send_dice_to_group(client, target_group, dice_sticker)

    client.disconnect()

if __name__ == "__main__":
    main()

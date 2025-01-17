import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load the MP3 file
pygame.mixer.music.load("sounds/success-1-6297.mp3")

# Play the MP3 file
pygame.mixer.music.play()

# Keep the program running while the sound is playing
while pygame.mixer.music.get_busy():  # Check if the music is still playing
    pass

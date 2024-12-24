import os

def play_sound(status: str):
    if status == "success":
        os.system("aplay sounds/success.wav")  # Success beep
    elif status == "error":
        os.system("aplay sounds/error.wav")    # Error beep
    else:
        os.system("aplay sounds/neutral.wav")  # Neutral beep

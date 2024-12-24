from time import sleep
from gpiozero import LED
import os

def show_status_on_display(message: str, status: str):
    print(f"Display: {message} ({status})")
    os.system(f'echo "{message}" > /dev/tty1')  # For connected display via serial

    # LED feedback (e.g., green for success, red for failure)
    green_led = LED(17)  # GPIO pin for green LED
    red_led = LED(27)    # GPIO pin for red LED

    if status == "success":
        green_led.on()
        sleep(2)
        green_led.off()
    elif status == "error":
        red_led.on()
        sleep(2)
        red_led.off()

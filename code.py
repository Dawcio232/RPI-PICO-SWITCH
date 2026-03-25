import time
import board
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from digitalio import DigitalInOut, Direction, Pull

# Wait for USB to be ready
time.sleep(1)

# Set up HID keyboard
kbd = Keyboard(usb_hid.devices)

# Set up buttons with internal pull-ups (pressed = low)
button15 = DigitalInOut(board.GP15)  # Alt+Tab
button15.direction = Direction.INPUT
button15.pull = Pull.UP

button14 = DigitalInOut(board.GP14)  # Toggle Win+Ctrl Right/Left
button14.direction = Direction.INPUT
button14.pull = Pull.UP

# Toggle state for GP14: True = right, False = left
right_arrow = True

print("Button HID ready. GP15: Alt+Tab, GP14: Win+Ctrl Right/Left (toggle)")

while True:
    # Check GP15 (Alt+Tab)
    if not button15.value:  # Pressed
        while not button15.value:
            pass  # Debounce
        kbd.press(Keycode.ALT, Keycode.TAB)
        kbd.release_all()

    # Check GP14 (toggle Right/Left)
    if not button14.value:  # Pressed
        while not button14.value:
            pass  # Debounce

        # Send based on toggle state
        if right_arrow:
            kbd.press(Keycode.LEFT_GUI, Keycode.LEFT_CONTROL, Keycode.RIGHT_ARROW)
            print("Sent Right")
        else:
            kbd.press(Keycode.LEFT_GUI, Keycode.LEFT_CONTROL, Keycode.LEFT_ARROW)
            print("Sent Left")
        kbd.release_all()

        # Toggle state
        right_arrow = not right_arrow

    time.sleep(0.01)


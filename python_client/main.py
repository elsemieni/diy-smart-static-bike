import PySimpleGUI as sg

import pyvjoy
from pynput.keyboard import Key, KeyCode, Controller

from inputs.JoyconInput import JoyconInput
from inputs.AndroidInput import AndroidInput
from inputs.CustomInput import CustomInput

# ===============================================================================
# Initialize variables

vjoy_enabled = False
inv_mode = False
cal_mode = 0
raw_value = 0
dead_zone = 0
max_value = 0
float_value = 0
yt_mode = False
yt_speed = 0  # 0 pause, 1 to 8 speeds.
selected_input_axis = "z"

HALF_AXIS = 16384
selected_axis = pyvjoy.HID_USAGE_Y


def pressButton(button, shift=False):
    print(button)
    if shift:
        keyboard.press(Key.shift)
    keyboard.press(button)
    keyboard.release(button)
    if shift:
        keyboard.release(Key.shift)

# ===============================================================================
# Initalize vJoy (if possible)
try:
    j = pyvjoy.VJoyDevice(1)
    j.set_axis(selected_axis, int(HALF_AXIS))
    vjoy_enabled = True
except:
    sg.popup("Ooops, no vJoy not found! Virtual gamepad will be disabled")

# ===============================================================================
# Start window
# ===============================================================================

keyboard = Controller()

input_devices = [
    "Joy-con (needs... well, a Joy-con connected to your PC)",
    "Android - gyroscope (needs a phone and an APK (included) )",
    "Custom (modify inputs/CustomInput.py at source code)"
]

layout = [[sg.Text('Select an input device')],
          [sg.Listbox(input_devices, size=(60, len(input_devices)), key='device_list')],
          [sg.Button('Ok')]]

window = sg.Window('Select an input device', layout)

selected_device = -1
while True:  # the event loop
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Ok':
        if values['device_list']:  # if something is highlighted in the list
            selected_device = window["device_list"].get_indexes()[0]
            break
window.close()

if selected_device == -1:
    quit(0)

# ===============================================================================
# Initalize device

if selected_device == 0:
    device = JoyconInput()
if selected_device == 1:
    device = AndroidInput()
if selected_device == 2:
    device = CustomInput()

if not device.initialize():
    sg.popup("Ooops, failed to initalize device! " + device.ERROR_MESSAGE)
    quit(-1)

# ===============================================================================
# Main window

axis_list = ["x","y","z"]

layout = [
    [sg.Text("Op mode        ", key="cal_indicator"), sg.Text("Normal axis  ", key="inv_indicator"),
     sg.Text("Youtube disabled  ", key="yt_indicator"), sg.Text("Raw Z value:"), sg.Text("0.0000", key="z_val")],
    [sg.Text("Using axis: "), sg.Combo(values=axis_list, size=(20,20), key='axis_selector', default_value = "z", readonly=True)],
    [sg.ProgressBar(1000, orientation='h', size=(45, 20), key='z_bar')],
    [sg.Button("Callibration mode", key="cal_button"), sg.Button("Reset callibration", key="reset_button"),
      sg.Button("Invert on/off", key="inv_button"), sg.Button("Youtube mode on/off", key="yt_button"), sg.Button("Exit", key="exit_button")],
    [sg.Text("Poor man's smart bike. 2021 Enzo Barbaguelatta - http://elsemieni.net/")]
]

window = sg.Window("Poor man´s smart bike", layout)


# ===============================================================================
# Main loop

while True:

    # =======================================
    # read
    raw_value = device.read(selected_input_axis)
    if inv_mode:
        raw_value *= -1

    # callibrate
    if cal_mode == 2:
        if raw_value < -(dead_zone + 100) and not inv_mode:
            inv_mode = True
            raw_value *= -1
            window["inv_indicator"].update("Inverted axis")
        if raw_value < -(dead_zone + 100) and inv_mode:
            inv_mode = False
            raw_value *= -1
            window["inv_indicator"].update("Normal axis")
        max_value = max(max_value, abs(raw_value))
    if cal_mode == 1:
        dead_zone = max(dead_zone, abs(raw_value))

    # Map between 0 and max_value
    try:
        float_value = raw_value / max_value
    except:
        float_value = 0
    if abs(raw_value) < dead_zone:
        float_value = 0

    # =======================================

    event, values = window.read(timeout=10)
    if event == sg.WIN_CLOSED or event == 'exit_button':
        break
    if event == "inv_button":
        inv_mode = not inv_mode
        if inv_mode:
            window["inv_indicator"].update("Inverted axis")
        else:
            window["inv_indicator"].update("Normal axis")
    if event == "cal_button":
        cal_mode += 1
        if cal_mode == 2:
            max_value = 0
            window["cal_indicator"].update("Max calibration")
        if cal_mode == 1:
            dead_zone = 0
            window["cal_indicator"].update("Dead zone calibration")
        if cal_mode == 3:
            cal_mode = 0
            window["cal_indicator"].update("Op mode")
    if event == "reset_button":
        cal_mode = 0
        raw_value = 0
        dead_zone = 0
        max_value = 0
        float_value = 0
    if event == "yt_button":
        yt_mode = not yt_mode
        if yt_mode:
            window["yt_indicator"].update("Youtube enabled")
            yt_speed = 0
        else:
            window["yt_indicator"].update("Youtube disabled")
    if event == "axis_selector":
        selected_input_axis = values['axis_selector']

    # =======================================

    if yt_mode:
        tmp = int(abs(float_value * 8))
        while tmp is not yt_speed:
            if tmp > yt_speed:
                if tmp > 0 and yt_speed == 0:
                    pressButton(Key.space)
                yt_speed += 1
                print("Speed: {}".format(yt_speed))
                pressButton(".", True)
            if tmp < yt_speed:
                if tmp == 0 and yt_speed != 0:
                    pressButton(Key.space)
                yt_speed -= 1
                print("Speed: {}".format(yt_speed))
                pressButton(",", True)

    # =======================================

    window["z_val"].update("{:.4f}".format(raw_value))
    window["z_bar"].update(500 + (float_value * 500))
    if vjoy_enabled:
        j.set_axis(selected_axis, int(HALF_AXIS + (float_value * HALF_AXIS)))

    # =======================================

window.close()
if vjoy_enabled:
    j.set_axis(selected_axis, int(HALF_AXIS))

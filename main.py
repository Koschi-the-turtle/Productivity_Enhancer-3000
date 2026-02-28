import time
import random
import webbrowser
import threading
import tkinter as tk
from tkinter import Tk, Canvas
from pynput import keyboard
import ctypes

LOSS_SPEED = 0.4 #speed at which the productivity bar goes down
GAIN_SPEED = 1.2 #speed at which it goes up

GETAJOB = 30 # warning pop up lvl
CHEESEBURGERPLS = 0 #Mcdonald job application lvl
BRIGHTFUTUREAHEAD = 100 #max bar lvl
CHECK_INTERVAL = 0.1 #ui refresh speed

MCDO_URLS = [
            "https://jobs.mchire.com/jobs?location_name=Shelburne%2C%20VT%2C%20USA&location_type=2&keyword=crew",
            "https://www.wikihow.com/Apply-at-McDonald%27s",
            "https://images.steamusercontent.com/ugc/28812445891088273/80FBC4918DFB81B32D71551D0CE30EB21283A695/"
]

productivity = BRIGHTFUTUREAHEAD
last_activity = time.time()
warning_triggered = False

#ui
root = Tk()
root.title("Productivity Bar")
root.geometry("500x135")
root.resizable(False, False)

canvas = Canvas(root, width=500, height=75, bg="#1e1e1e", highlightthickness=0)
canvas.pack()

#(un)employment rate slider
slider_frame = tk.Frame(root, bg = "#1e1e1e", highlightthickness=0, bd = 0)
slider_frame.pack(fill = "x", pady = 0)

def update_loss_speed(value):
    global LOSS_SPEED
    LOSS_SPEED = float(value)

loss_slider = tk.Scale(
    master = slider_frame,
    from_ = 0.1,
    to = 3.0,
    resolution = 0.1,
    orient = "horizontal",
    length = 480,
    font = ("Arial", 11),
    label = "(un)emlpoyment rate",
    command = update_loss_speed,
    bg = "#1e1e1e",
    fg = "#ffffff",
    troughcolor = "#333333",
    highlightthickness = 0
)
loss_slider.set(LOSS_SPEED)
loss_slider.pack(pady=5)

#productivity bar
def draw_bar():
    canvas.delete("all")
    pct = max(0, min(productivity, BRIGHTFUTUREAHEAD)) / BRIGHTFUTUREAHEAD
    bar_width = int(pct * 480)
    #↓bar color gradually changes based on productivity percentage↓
    if pct >= 0.5:
        t = (pct - 0.5) * 2
        r = int(255 * (1-t))
        g = 255
        b = 0
    else:
        t = pct * 2
        r = 255
        g = int(255 * t)
        b  = 0
    
    color = f"#{r:02x}{g:02x}{b:02x}"

    canvas.create_rectangle(10, 30, 490, 60, fill="#333333", outline="")
    canvas.create_rectangle(10, 30, 10 + bar_width, 60, fill=color, outline="")

    canvas.create_text(
        250, 15,
        text=f"Productivity: {int(productivity)}%",
        fill="#ffffff",
        font = ("Arial", 12, "bold")
    )
                             

#keyboard tracking
def on_key_press(key):
    global productivity, last_activity
    productivity = min(BRIGHTFUTUREAHEAD, productivity + GAIN_SPEED)
    last_activity = time.time()

keyboard.Listener(on_press=on_key_press).start()

#the steak of the burger (aka the main shi-)
def update_loop():
    global productivity, warning_triggered

    while True:
        time.sleep(CHECK_INTERVAL)
        idle_time = time.time() - last_activity
        if idle_time > 1.0:
            productivity -= LOSS_SPEED
        else:
            productivity = min(BRIGHTFUTUREAHEAD, productivity + GAIN_SPEED * CHECK_INTERVAL)
        productivity -= LOSS_SPEED * CHECK_INTERVAL
        productivity = max(CHEESEBURGERPLS, min(BRIGHTFUTUREAHEAD, productivity))

        #warning pop-up
        if productivity <= GETAJOB and not warning_triggered:
            warning_triggered = True
            ctypes.windll.user32.MessageBoxW(
                0,
                "!WARNING⚠️: Your screen seems to be brighter than your foreseeable future⚠️\n"
                ".Return to work before you end up at the nearest McDonald® in a 10km radius\n"
                "™This alert has been issued to you by the US Department of Homeland Security",
                0
            )

        if productivity <= CHEESEBURGERPLS:
            url = random.choice(MCDO_URLS)
            webbrowser.open(url)
            warning_triggered = False
            productivity = BRIGHTFUTUREAHEAD #productivity resets after mcdonald application

        root.after(0, draw_bar)

threading.Thread(target=update_loop, daemon = True).start()

draw_bar()
root.mainloop()
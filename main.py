import time
import webbrowser
import threading
from tkinter import Tk, Canvas
from pynput import keyboard
import ctypes

LOSS_SPEED = 0.4 #speed at which the productivity bar goes down
GAIN_SPEED = 1.2 #speed at which it goes up

GETAJOB = 30 # warning pop up lvl
CHEESEBURGERPLS = 0 #Mcdonald job application lvl
BRIGHTFUTUREAHEAD = 100 #max bar lvl
CHECK_INTERVAL = 0.1 #ui refresh speed

MCDO_URL1= "https://www.mchire.com/co/McDonalds2692/Job?job_id=PDX_MC_5D0FA666-7DC8-4EB2-81DA-B39422F01A7E_69251"
MCDO_URL2 = "https://www.wikihow.com/Apply-at-McDonald%27s"
MCDO_URL3 = "https://images.steamusercontent.com/ugc/28812445891088273/80FBC4918DFB81B32D71551D0CE30EB21283A695/"

productivity = BRIGHTFUTUREAHEAD
last_activity = time.time()
warning_triggered = False

#ui
root = Tk()
root.title("Productivity Bar")
root.geometry("500x80")
root.resizable(False, False)

canvas = Canvas(root, width=500, height=80, bg="#1e1e1e", highlightthickness=0)
canvas.pack()

def draw_bar():
    """Redraw the productivity bar UI"""
    canvas.delete("all")
    
    pct = max(0, min(productivity, BRIGHTFUTUREAHEAD)) / BRIGHTFUTUREAHEAD
    bar_width = int(pct*480)

    canvas.create_rectangle(10, 30, 490, 60, fill="#333333", outline="")
    if pct > 0.6:
        color = "#4caf50"
    elif pct > 0.3:
        color = "#ddc107"
    else:
        color = "#f44336"

    canvas.create_rectangle(10, 30, 10 + bar_width, 60, fill=color, outline="")
    canvas.create_text( 
        250, 15,
        text=f"Productivity: {int(productivity)}%",
        fill="white",
        font=("Arial", 12, "bold")
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
        productivity -= LOSS_SPEED * idle_time * CHECK_INTERVAL

        productivity = max(CHEESEBURGERPLS, min(BRIGHTFUTUREAHEAD, productivity))
        if productivity <= GETAJOB and not warning_triggered:
            warning_triggered = True
            ctypes.windl.user32.MesssageBoxW(
                0,
                "⚠️ WARNING: Your screen seems to be brighter than your future.\n"
                "Return to work before you end up at the nearest McDonald®.\n"
                "Productivity Alert provided by the Productivity Enhancer 3000™",
                0
            )

            if productivity <= CHEESEBURGERPLS:
                webbrowser.open(MCDO_URL1)
                warning_triggered = False
                productivity = BRIGHTFUTUREAHEAD #productivity resets after mcdonald application

                draw_bar()

            threading.Thread(target=update_loop, daemon = True).start()

            draw_bar()
            root.mainloop()

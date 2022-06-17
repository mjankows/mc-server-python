import tkinter as tk
import datetime
import _thread
from gpiozero import CPUTemperature
from tkinter import ttk
from subprocess import call
from json import loads
from time import sleep

SERVER_GUI = tk.Tk()
FRAME = ttk.Frame(SERVER_GUI, padding=500)
FRAME.grid()
SERVER_UP = False

def temperature_loop():
    while True:
        sleep(1)


def startup_shutdown_loop():
    global SERVER_UP
    while True:
        sleep(60)
        if datetime.datetime.now().hour < 12  and SERVER_UP:
            SERVER_UP = False
            call("stop &")
        elif datetime.datetime.now().hour >=12 and not SERVER_UP:
            SERVER_UP = True
            call("java -Xmx2048M -Xmn2048M -jar server.jar nogui &")
        else:
            print(datetime.datetime.now())


def add_command_button(text, command, col, row):
    ttk.Button(FRAME, text = text, command = lambda: call(command)).grid(
        column=col, row=row)
        
def window_setup(commands):
    ttk.Label(FRAME, text="Matthew's Minecraft Server Gui").grid(column=0, row=0)
    for i in commands:
        for j, item in enumerate(commands[i]):
            add_command_button(item, commands[i][item],i, j+1)
    _thread.start_new_thread(startup_shutdown_loop, ())
    tk.mainloop()






def main():
    call("vcgencmd measure_temp &")
    with open('commands') as f:
        data = f.read()
    print(data)
    data = loads(data)
    print(data)
    print(datetime.datetime.now())
    for i, item in enumerate(data):
        print(i, data[item])
    window_setup(data)


if __name__ == "__main__":
    main()
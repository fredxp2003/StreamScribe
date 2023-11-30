import requests
import threading
import vlc
from tkinter import *
from tkinter import simpledialog
import datetime
import time
import os
import subprocess

print("Welome to StreamScribe! (version 1.0.0-beta2): The GUI Update")

try:
    with open(".url", "r") as f:
        url = f.read()
except FileNotFoundError:
    with open(".url", "a") as f: 
        pass  

    url = ""

recording_flag = True
filename_input = None
# See if the output folder exists, if not, create it
path = os.path.join(os.getcwd(), "output")
if not os.path.exists(path):
    os.mkdir(path)


def vlc_init(url):
    instance = vlc.Instance()
    player=instance.media_player_new()
    media=instance.media_new(url)
    player.set_media(media)
    return player

def start_recording():
    global recording_flag, filename_input
    recording_flag = True
    filename_input = simpledialog.askstring("Filename", "Enter a filename for the recording:")

    #thread instance
    new_recording_thread = threading.Thread(target=record)
    new_recording_thread.start()

def timer():
    global recording_flag
    seconds = 0
    while recording_flag:
        time.sleep(1)
        seconds += 1
        minutes = seconds // 60
        seconds_part = seconds % 60
        elapsed_time = f"{minutes:02d}:{seconds_part:02d}"
        label_text.set(f"Recording...  {elapsed_time}")
    label_text.set(f"File saved as {filename}.mp3")

def record():
    global recording_flag, filename_input, filename
    filename = filename_input if filename_input else datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    url = url_box.get()
    with open(".url", "w") as f:
        f.write(url)

    # Initialize VLC
    player = vlc_init(url)

    # init stream 
    stream = requests.get(url, stream=True)
    player.play()

    label_text.set(f"Recording...  00:00")
    threading.Thread(target=timer).start()
    OUTPUT_PATH = os.path.join("output", f"{filename}.mp3")
    with open(OUTPUT_PATH, "wb") as f:
        for chunk in stream.iter_content(chunk_size=4096):
            if not recording_flag:
                player.stop()
                break  
            if chunk:
                f.write(chunk)
    print("Done recording!")

def stop():
    global recording_flag
    print("Stopping...")
    recording_flag = False

def open_output_folder():
    # WINDOWS
    if os.name == 'nt':
        os.startfile(path)
    # MACOS / LINUX
    elif os.name == 'posix':
        subprocess.call(['open', path])


# The Tkinter stuff :)
root = Tk()
root.title("StreamScribe")
root.iconbitmap("icon.ico")
root.geometry("500x250")

root.configure(bg='#333645') 

main_frame = Frame(root, bg='#333645')
main_frame.pack(padx=20, pady=20)

label_text = StringVar()
label_text.set("Welcome to StreamScribe!")

title_font = ("Arial", 18, "bold")
da_label = Label(main_frame, textvariable=label_text, bg='#333645', fg='#FFFFFF', font=title_font)
da_label.grid(row=0, column=0, columnspan=2, pady=10) 

button_font = ("Arial", 16)
record_button = Button(main_frame, text="Record", command=start_recording, font=button_font, bg='#007BFF', fg='#FFFFFF', relief=FLAT)
record_button.grid(row=1, column=0, padx=10, pady=10)  

url_font = ("Arial", 14)
url_box = Entry(main_frame, width=40, font=url_font)
url_box.grid(row=2, column=0, columnspan=2, pady=10)
url_box.insert(0, url)

stop_button = Button(main_frame, text="Stop", command=stop, font=button_font, bg='#FF6347', fg='#FFFFFF', relief=FLAT)
stop_button.grid(row=1, column=1, padx=10, pady=10)

open_folder_button = Button(main_frame, text="Open Folder", command=open_output_folder, font=button_font, bg='#28B463', fg='#FFFFFF', relief=FLAT)
open_folder_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
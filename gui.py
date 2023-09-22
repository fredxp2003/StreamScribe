import requests
import threading
# import configparser as config
import vlc
from tkinter import *
from tkinter import simpledialog
import os
import datetime

print("Welome to StreamScribe! (version 1.0.0-beta1): The GUI Update")

# Read from settings file
try:
    with open(".url", "r") as f:
        url = f.read()
except FileNotFoundError:
    # Create file if it doesn't exist
    with open(".url", "a") as f: 
        pass  

    url = ""
    

# Initialize VLC
def vlc_init(url):
    instance = vlc.Instance()
    player=instance.media_player_new()
    media=instance.media_new(url)
    player.set_media(media)
    return player

recording_flag = True

filename_input = None  # This variable will store the filename provided by the user

def start_recording():
    global recording_flag, filename_input
    recording_flag = True

    # Popup a dialog to get the filename from the user
    filename_input = simpledialog.askstring("Filename", "Enter a filename for the recording:")
    
    if not filename_input:  # If user presses Cancel or provides no name
        print("Recording cancelled.")
        return

    # Create and start a new thread instance
    new_recording_thread = threading.Thread(target=record)
    new_recording_thread.start()



def record():
    global recording_flag, filename_input, filename
    # Use the filename provided by the user
    filename = filename_input if filename_input else datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    # Get url from text box
    url = url_box.get()
    # Write url to file
    with open(".url", "w") as f:
        f.write(url)
    # Initialize VLC
    player = vlc_init(url)
    # init stream 
    stream = requests.get(url, stream=True)
    # Start recording
    player.play()
    with open(f"{filename}.mp3", "wb") as f:
        for chunk in stream.iter_content(chunk_size=2048):
            if not recording_flag:  # Check if recording should stop
                player.stop()  # Stop the VLC player
                break  # Exit loop
            if chunk:
                f.write(chunk)
    print("Done recording!")

def stop():
    global recording_flag
    print("Stopping...")
    recording_flag = False  # Set the flag to stop recording
    
    # Update the label's text to the filename
    now = datetime.datetime.now()
    label_text.set(f"Saved: {filename}.mp3")

    

recording = threading.Thread(target=record)



# GUI
root = Tk()
root.title("StreamScribe")
root.geometry("500x250")

# Set a background color for the root window
root.configure(bg='#333645') 

# Create a frame to contain our widgets
main_frame = Frame(root, bg='#333645')
main_frame.pack(padx=20, pady=20)

# Initialize a StringVar for the label's text
label_text = StringVar()
label_text.set("Welcome to StreamScribe!")  # default text

# Use a label with a larger font and bind it to the StringVar
title_font = ("Arial", 18, "bold")
myLabel = Label(main_frame, textvariable=label_text, bg='#333645', fg='#FFFFFF', font=title_font)
myLabel.grid(row=0, column=0, columnspan=2, pady=10) 

# Adjusted button styles
button_font = ("Arial", 16)
myButton = Button(main_frame, text="Record", command=start_recording, font=button_font, bg='#007BFF', fg='#FFFFFF', relief=FLAT)
myButton.grid(row=1, column=0, padx=10, pady=10)  

# Text box for URL with some padding
url_font = ("Arial", 14)
url_box = Entry(main_frame, width=40, font=url_font)
url_box.grid(row=2, column=0, columnspan=2, pady=10)
url_box.insert(0, url)

# Stop recording button with style
stopButton = Button(main_frame, text="Stop", command=stop, font=button_font, bg='#FF6347', fg='#FFFFFF', relief=FLAT)
stopButton.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
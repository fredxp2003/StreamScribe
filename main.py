import requests
import threading
import configparser as config
from tkinter import *

config = config.ConfigParser()
config.read("config.ini")
url = config["settings"]["url"]
stream = requests.get(url, stream=True)

print("Welome to StreamScribe! (version 0.0.1)")


def record(stream, filename):
    with open(f"{filename}.mp3", "wb") as f:
        for chunk in stream.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def settings():
    print("Settings")
    choice = input("Would you like to change the URL? (y/n): ")
    if choice.lower() == "y":
        url = input("Enter a new URL: ")
        config["settings"]["url"] = url
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        print("Settings saved!")
        return
    else:
        print("No changes were made.")
        return


# Main loop
while True:
    print(
        """
    1. Record
    2. Settings
    3. Exit
    """
    )
    choice = input("Enter a choice: ")
    if choice == "1":
        filename = input("Enter name for recording: ")
        thread = threading.Thread(target=record, args=(stream, filename))
        thread.start()

        print(f"Recording started on {url}.")
        input("Press enter to stop recording...")
        stream.close()
        print(f"Recording stopped.  File saved as {filename}.mp3")

    elif choice == "2":
        settings()

    elif choice == "3":
        exit()
    else:
        print("Invalid choice. Please try again.")
        continue

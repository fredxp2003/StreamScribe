import requests
import threading
import configparser as config
import vlc

print("Welome to StreamScribe! (version 0.0.2)")

# Read config file
config = config.ConfigParser()
config.read("config.ini")
url = config["settings"]["url"]


# Initialize VLC
instance = vlc.Instance()
player=instance.media_player_new()
media=instance.media_new(url)
player.set_media(media)

def record(stream, filename):
    threading.Thread(target=player.play).start()
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
        stream = requests.get(url, stream=True)
        thread = threading.Thread(target=record, args=(stream, filename))
        thread.start()

        print(f"Recording started on {url}.")
        input("Press enter to stop recording...")
        stream.close()
        player.stop()
        print(f"Recording stopped.  File saved as {filename}.mp3")

    elif choice == "2":
        settings()

    elif choice == "3":
        exit()
    else:
        print("Invalid choice. Please try again.")
        continue

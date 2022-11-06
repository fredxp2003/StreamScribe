import requests
import threading
import configparser as config
from tkinter import *

config = config.ConfigParser()
config.read('config.ini')
url = config['settings']['url']
stream = requests.get(url, stream=True)

print('Welome to StreamScribe! (version 0.0.1)')
filename = input('Enter a filename: ')

def record(stream, filename):
    with open(f'{filename}.mp3', 'wb') as f:
        for chunk in stream.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

thread = threading.Thread(target=record, args=(stream, filename))
thread.start()

print('Recording...')
print('Press enter to stop recording.')
input()
stream.close()
print('Recording stopped.')
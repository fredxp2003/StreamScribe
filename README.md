# StreamScribe

StreamScribe is a simple, lightweight, and easy to use application that allows you to record audio streams from the internet.  Currently, it is a CLI application, but a GUI is planned for the future.

## Installation
Be sure that Python 3.6+ is installed on your system.  Then, install the dependencies with `pip install -r requirements.txt`.  Finally, run `python3 streamscribe.py` to start the application.

## Setup
StreamScribe uses a configuration file to store the stream URL.  The default url points to WXOU, a radio station at Oakland University.  To change the URL, edit the select the second option in the main menu when running the application.  Then enter the URL of the stream you want to record.

## Usage
To record a stream, select the first option in the main menu.  The stream will be recorded to a file in the same directory as the application.  The file will be named `[chosen name].mp3` by default.

## License
StreamScribe is licensed under the MIT License.  See the LICENSE file for more information.
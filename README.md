# BTTtimer
A timer for Super Mario Odyssey BTT segements

Current version: 0.1 Alpha

## Installation
You need Python 3 to use BTTtimer, preferrably the newest release.
The script is to be built into an executable in the future, but for now a Python Script will do for testing.
To install the required dependencies you'll need to run a few commands:
```
pip install youtube_dl
pip install imageio
```
You will need to manually install 2 dependencies, ffmpeg and fast-colorthief.
Download ffmpeg [from here](https://ffmpeg.org/download.html) and install to PATH.
Follow [these instructions](https://github.com/bedapisl/fast-colorthief) to install fast-colorthief. On MacOS and Linux, you can run a simple pip command like above - on Windows you'll need to manually install it.

## Usage
With a URL:
```
btttimer.py [URL] [Start Method] [End Method]
```

With a file (use the actual word "file", not the path. Put your video in the BTTtimer directory.):
```
btttimer.py file [Start Method] [End Method]
```

The only working start and end method as of 0.1a is f (fadeout). You can find the upcoming list by running
```
btttimer.py -h
```

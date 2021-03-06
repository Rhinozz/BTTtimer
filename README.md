# BTTtimer
A timer for Super Mario Odyssey BTT segements

Current version: 0.1.1 Alpha

## Installation
Note: You need to be on Windows for the official installation. If you are not on Windows, you need to build it from the source - see **Dev Installation**.

The only prerequisite needed for BTTtimer is FFmpeg. Download it [here](https://github.com/BtbN/FFmpeg-Builds/releases) and install onto PATH.

Then, download and run the executable. 

## Dev Installation
You need Python 3 to use BTTtimer, preferrably the newest release.

To install the required dependencies you'll need to run a few commands:
```
pip install youtube_dl
pip install imageio
```
You will need to manually install 2 dependencies, ffmpeg and fast-colorthief.

Download ffmpeg [here](https://github.com/BtbN/FFmpeg-Builds/releases) and install onto PATH.

Follow [these instructions](https://github.com/bedapisl/fast-colorthief) to install fast-colorthief. On MacOS and Linux, you can run a simple pip command like above - on Windows you'll need to manually install it.

## Usage
Note: When using the developer version, replace `btttimer.exe` with `btttimer.py`.

With a URL:
```
btttimer.exe [URL] [Start Method] [End Method]
```

With a file (use the actual word "file", not the path. Put your video in the BTTtimer directory.):
```
btttimer.exe file [Start Method] [End Method]
```

The only working start and end method as of 0.1.2a is f (fadeout). You can find the upcoming list by running
```
btttimer.exe -h
```

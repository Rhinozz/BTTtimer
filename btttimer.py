from __future__ import unicode_literals
from shutil import copy2, rmtree
import os, glob, argparse
from PIL import Image
import youtube_dl, fast_colorthief, imageio

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='[Required] Your input URL. If you have downloaded the file, put it in the same directory as this script and type "file" in the place of your URL.')
parser.add_argument('startmethod', type=str, help='[Required] Your start timing method. Can only be f (fadeout) for now, but in the future m (moon tick), c (cutscene fadeout), g (globe cutscene), w (warp), and c (capture glow) will be implemented.')
parser.add_argument('endmethod', type=str, help='[Required] Your end timing method. Can only be f (fadeout) for now, but in the future m (moon tick), c (cutscene fadeout), g (globe cutscene), w (warp), and c (capture glow) will be implemented.')
args = parser.parse_args()

# download video
print('Downloading video')
workingDir = os.getcwd()
for filename in os.listdir(workingDir):
    if filename.endswith(".mp4"):
        os.rename(filename, 'twtdl.mp4')
    else:
        continue
if args.input != "file":
    ydl_opts = {
        'format': 'bestvideo/best',
        'outtmpl': "twtdl.mp4",
        'quiet': True,
        'no_warnings': True,
    }
   
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.input])

# split video into frames
os.system("ffmpeg -i twtdl.mp4 %04d.png")
tempDir = workingDir + "\\tmp"
os.mkdir(tempDir, 0o666)
for file in os.listdir(workingDir):
    if file.endswith(".png"):
        copySrc = workingDir + "\\" + file
        copyDest = tempDir + "\\" + file
        copy2(copySrc, copyDest)

# check if methods are the same
if args.startmethod == args.endmethod:
    sameMethods = True
else:
    sameMethods = False

# scan for first load frame
startDone = False
for n in range(2):
    # detects fadeout
    if args.startmethod == "f":
        f = None
        firstBefore = None
        print('Scanning for loads')
        for file in os.listdir(workingDir):
            if file.endswith(".png"):
                fileFull = workingDir + "\\" + file
                dom = fast_colorthief.get_dominant_color(fileFull, quality=1)
                domStr = ''.join(map(str, dom))
                if domStr != "444":
                    os.remove(fileFull)
                    continue
                im = imageio.imread(fileFull, pilmode='RGB')
                color = tuple(im[360][639])
                colorStr = ''.join(map(str, color))
                if colorStr != "000":
                    os.remove(fileFull)
                    continue
                if sameMethods is True:
                    fClean1 = os.path.split(fileFull)[1]
                    fClean = fClean1.replace('.png', '')
                    fMinus = int(fClean) - 1
                    if f == None:
                        f = fClean
                    else:
                        if int(f) == int(fMinus):
                            f = fClean
                            os.remove(fileFull)
                        else:
                            f = fClean
                else:
                    if firstBefore == None:
                        firstBefore = True
                    else:
                        os.remove(fileFull)
            else:
                continue

# get final time
files = os.listdir(workingDir)
for i in files:
    if i.endswith(".png"):
        pass
    else:
        files.remove(i)
        continue
itemsClean1 = files[0].replace('.png', '')
firstTime = int(itemsClean1) / 30
itemsClean = files[1].replace('.png', '')
secondTime = int(itemsClean) / 30
finalTime1 = secondTime - firstTime
finalTime = round(finalTime1, 3)
print("Time: " + str(finalTime))
firstRound = round(firstTime - 0.0333333, 3)
secondRound = round(secondTime - 0.0333333, 3)
print("First Frame: " + str(firstRound))
print("Last Frame: " + str(secondRound))

# remove temporary files
videoFile = workingDir + "\\twtdl.mp4"
os.remove(videoFile)
os.chdir(workingDir)
for frame in glob.glob("*.png"):
    os.remove(frame)
rmtree(tempDir)
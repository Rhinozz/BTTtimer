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
workingDir = os.getcwd()  # current directory
for filename in os.listdir(workingDir):
    if filename.endswith(".mp4"):
        os.rename(filename, 'twtdl.mp4')  # renames file
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
        ydl.download([args.input])  # downloads file

# split video into frames
os.system("ffmpeg -i twtdl.mp4 %04d.png")
tempDir = workingDir + "\\tmp"
os.mkdir(tempDir, 0o666)  # makes temporary directories
for file in os.listdir(workingDir):
    if file.endswith(".png"):
        copySrc = workingDir + "\\" + file
        copyDest = tempDir + "\\" + file
        copy2(copySrc, copyDest)  # copies frames into temp

# check if methods are the same
if args.startmethod == args.endmethod:
    sameMethods = True
else:
    sameMethods = False

# detects fadeout
def fadeout():
    f = None  # variable used as current file in detection loop
    firstBefore = None
    print('Scanning for loads')
    for file in os.listdir(workingDir):
        if file.endswith(".png"):  # for all frames
            fileFull = workingDir + "\\" + file
            dom = fast_colorthief.get_dominant_color(fileFull, quality=1)  # gets dominant color
            domStr = ''.join(map(str, dom))
            if domStr != "444":  # if dominant color isn't black
                os.remove(fileFull)
                continue
            im = imageio.imread(fileFull, pilmode='RGB')
            color = tuple(im[360][639])  # get color of middle pixel
            colorStr = ''.join(map(str, color))
            if colorStr != "000":  # if color isn't black
                os.remove(fileFull)
                continue
            color2 = tuple(im[360][641])
            color2Str = ''.join(map(str, color))  # gets color of next to middle pixel for 60fps adjusting
            if color2Str != "000":
                if startDone == False:
                    adjustFirst = 0.0166667
                else:
                    adjustSecond = 0.0166667
            else:
                if startDone == False:
                    adjustFirst = 0
                else:
                    adjustSecond = 0
            if sameMethods is True:
                fClean1 = os.path.split(fileFull)[1]
                fClean = fClean1.replace('.png', '')  # gets current time
                fMinus = int(fClean) - 1
                if f == None:  # if first frame
                    f = fClean  # sets first frame
                else:
                    if int(f) == int(fMinus):  # if frame is not the first frame of fadeout
                        f = fClean
                        os.remove(fileFull)  # remove frame, leaving first and last frames
                    else:
                        f = fClean
            else:
                # going to be implemented soon
                # cross-method variables
                print("This feature hasn't been implemented yet.")
        else:
            continue

# get frames
startDone = False  # checks if loop is in first or second time
for n in range(2):
    if startDone == False:
        if args.startmethod == "f":
            fadeout()
       
        startDone = True
    else:
        if args.endmethod == "f":
            fadeout()
        
        break

# get final time
files = os.listdir(workingDir)
for i in files:  # lists 2 remaining frames
    if i.endswith(".png"):
        pass
    else:
        files.remove(i)
        continue
itemsClean1 = files[0].replace('.png', '')
firstTime = int(itemsClean1) / 30  # gets first time
itemsClean = files[1].replace('.png', '')
secondTime = int(itemsClean) / 30  # gets second time
finalTime1 = secondTime - firstTime
finalTime = round(finalTime1, 3)  # gets final time
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
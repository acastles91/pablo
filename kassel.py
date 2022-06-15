import cv2
import os
from picamera import PiCamera
from time import sleep
from threading import Thread
import shutil
import subprocess
import shlex

#import screeninfo
# import pyglview


class ThreadedCamera(object):
    def __init__(self):
        if (os.path.exists(video_dir)):
            shutil.rmtree(video_dir)
        os.makedirs(video_dir)
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.start_preview(alpha=255)

        self.camera.framerate = 25
        self.thread = Thread(target=self.record_videos, args=())
        self.thread.daemon = True
        self.thread.start()

    def record_videos(self):
        self.camera.start_recording(video_dir + '/000.h264', quality = video_quality)
        i = 1
        while True:
            self.camera.wait_recording(video_len_sec)
            self.camera.split_recording(video_dir + '/%03d.h264' % i)
            i = i + 1
        self.camera.stop_recording()

class ThreadedPlayer(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1/25
        self.FPS_MS = int(self.FPS * 1000)

        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.status = False
        self.frame = None

    def update(self):
        while True:
            if self.capture.isOpened():
                ret = self.capture.grab()
                if not ret:
                    self.capture.release()
                    return 
                (self.status, self.frame) = self.capture.retrieve()
            #sleep(self.FPS)
            sleep(25)
    def grab_frame(self):
        if (self.status):
            return self.frame
        return None

    def is_opened(self):
        return self.capture.isOpened()
    
    def clean_up(self):
        self.capture.release()

def externalPlayerCaller(video):

    cmd = ["ffplay", video]
    subprocess.call(cmd)

def getVideoList():
    files = []
    for file in os.listdir(video_dir):
        if file.endswith(".h264"):
            files.append(os.path.join(video_dir, file))
    files.sort()
    return files

def playVideoList(files):
    i = len(files)
    speed = 1
    for video in files:
        print("Playing video: " + video + " and skipping every " + str(i)  + "th frame")
        # cap = cv2.VideoCapture(video)
        # def loop():
            # check, frame = cap.read()
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # if check:
                # viewer.set_image(frame)
        # viewer.set_loop(loop)
        # viewer.start()
        cmd = ["mpv", "--screen=0", "--fs",  "--fs-screen=1", "--speed=" + str(speed), video]
        subprocess.call(cmd)
        #thread = Thread(target=externalPlayerCaller, args=video)
        #thread.daemon = True
        #thread.start()
        '''threadplayer = ThreadedPlayer(video)
        cv2.namedWindow("playback", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("playback", cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        
        #cv2.moveWindow("playback", -900, 0)
                       
                
        while threadplayer.is_opened():
            frame = threadplayer.grab_frame()
            
            if (frame is not None):
                cv2.moveWindow("playback", 1800,900) 
                cv2.imshow("playback", frame,)
                
                
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                print("hit wait key breaking")
                threadplayer.clean_up()
                break
        threadplayer.clean_up()
'''
        i = i - 1

# Parameters
win_name = "playback"
cv2.namedWindow("playback", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("playback", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#cv2.namedWindow("playback", cv2.WINDOW_NORMAL)
#cv2.setWindowProperty("playback", cv2.WND_PROP_OPENGL, cv2.WINDOW_NORMAL)
video_quality = 30
video_dir = os.getcwd() + "tmp/recordings/"
video_len_sec = 60
blackBackground = "wp2787656.jpg"
backgroundCommand = ["nohup", "feh", "--geometry", "+0+0", "-F", str(blackBackground), ">", "/dev/null"]
#backgroundCommand = ["nohup", "feh", "--geometry", "+0+0", "-F", str(blackBackground), "&" ]
subprocess.Popen(backgroundCommand)
print("background called")
#cv2.destroyAllWindows()
threadedCamera = ThreadedCamera()
# viewer = pyglview.Viewer()
# viewer.enable_fullscreen()
# viewer.set_window_name(win_name)

sleep(video_len_sec + 1)
print("after sleep")
files = getVideoList()
print(files)

i = 1
#test = os.getcwd() + "/tmp/recordings/0.h264"
#threadedPlayer = ThreadedPlayer(test)

while True:
    files = getVideoList()
    files = files[0:i]
    print(files)
    playVideoList(files)
    i = i + 1
'''while True:
    cv2.VideoCapture(test + "0.h264")
#cv2.destroyAllWindows()
'''

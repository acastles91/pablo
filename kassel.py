import cv2
import os
from picamera import PiCamera
from time import sleep
from threading import Thread
import shutil
#import screeninfo
# import pyglview


# Parameters
win_name = "playback"
cv2.namedWindow("playback", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("playback", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)




video_quality = 30
video_dir = os.getcwd() + "/tmp/recordings/"
video_len_sec = 5

cv2.destroyAllWindows()

class ThreadedCamera(object):
    def __init__(self):
        if (os.path.exists(video_dir)):
            shutil.rmtree(video_dir)
        os.makedirs(video_dir)
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.start_preview(alpha=255)

        self.thread = Thread(target=self.record_videos, args=())
        self.thread.daemon = True
        self.thread.start()

    def record_videos(self):
        self.camera.start_recording(video_dir + '/0.h264', quality = video_quality)
        i = 0
        while True:
            self.camera.wait_recording(video_len_sec)
            self.camera.split_recording(video_dir + '/%d.h264' % i)
            i = i + 1
        self.camera.stop_recording()

class ThreadedPlayer(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1/30
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
            sleep(self.FPS)

    def grab_frame(self):
        if (self.status):
            return self.frame
        return None

    def is_opened(self):
        return self.capture.isOpened()
    
    def clean_up(self):
        self.capture.release()


threadedCamera = ThreadedCamera()
# viewer = pyglview.Viewer()
# viewer.enable_fullscreen()
# viewer.set_window_name(win_name)

sleep(video_len_sec + 1)
print("after sleep")

def getVideoList():
    files = []
    for file in os.listdir(video_dir):
        if file.endswith(".h264"):
            files.append(os.path.join(video_dir, file))
    files.sort()
    return files

def playVideoList(files):
    i = len(files)
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

        threadplayer = ThreadedPlayer(video)
        cv2.namedWindow("playback", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("playback", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                
        while threadplayer.is_opened():
            frame = threadplayer.grab_frame()
            
            if (frame is not None):
                cv2.imshow("playback", frame,)
                
                
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                print("hit wait key breaking")
                threadplayer.clean_up()
                break
        threadplayer.clean_up()

        i = i - 1

files = getVideoList()
print(files)

i = 1

while True:
    files = getVideoList()
    files = files[0:i]
    print(files)
    playVideoList(files)
    i = i + 1


cv2.destroyAllWindows()

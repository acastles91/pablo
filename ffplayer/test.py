from ffpyplayer.player import MediaPlayer
import time

filename = "20second.mp4"
player = MediaPlayer(filename)
val = ''
while val != 'eof':
    frame, val = player.get_frame()
    if val != 'eof' and frame is not None:
        img, t = frame
        print img, t
        #display img

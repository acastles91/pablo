import os
import subprocess
import shlex

cmd = shlex.split("ffplay 20second.mp4")
subprocess.call(cmd, stdin=None, stdout=None, stderr=None, shell=False)


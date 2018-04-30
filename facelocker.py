# !/usr/bin/python3
import logging
import os
import platform
import subprocess
import time

import cv2
import face_recognition

# Cross-platform
MAC_LOCK_CMD = r"/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession \
 -suspend"
LINUX_LOCK_CMD = r"dde-lock > /dev/null 2>&1"

WIN_LOCK_CMD = r"rundll32.exe user32.dll,LockWorkStation"

# Config
TMP_PIC_FILE = r"face.png"


def run_facelocker(lock_func):
    while True:
        # if True:
        if not capture_face():
            lock_func()
        time.sleep(5)


# capture face
def capture_face():
    face = False
    camera = cv2.VideoCapture(0)
    for i in range(10):
        ret, image = camera.read()
        if ret is None:
            return False
        cv2.imwrite(TMP_PIC_FILE, image)
        image = face_recognition.load_image_file(TMP_PIC_FILE)
        face_locations = face_recognition.face_locations(image)
        if face_locations:
            face = True
            break
        time.sleep(0.1)
    del camera
    return face

# get linux lock


def linux_lockcmd():
    return LINUX_LOCK_CMD

# get lock


def get_lock():
    lock_cmd = ""
    sys = platform.system()
    if sys == "Windows":
        lock_cmd = WIN_LOCK_CMD
    elif sys == "Darwin":
        lock_cmd = MAC_LOCK_CMD
    elif sys == "Linux":
        lock_cmd = linux_lockcmd()
    else:
        print("Unknown system")
        exit(1)

    def lock_func():
        subprocess.call(lock_cmd, shell=True)
    return lock_func


if __name__ == "__main__":
    run_facelocker(get_lock())

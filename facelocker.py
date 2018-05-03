#!/usr/bin/python3
import getopt
import platform
import subprocess
import time

import cv2
import face_recognition

''' ==================================================================== '''
# Cross-platform
UBUNTU_LOCK_CMD = r"gnome-screensaver-command --lock"
WIN_LOCK_CMD = r"rundll32.exe user32.dll,LockWorkStation"
MAC_LOCK_CMD = r"/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession \
 -suspend"

# Config
TMP_PIC_FILE = r"face.png"
CAPTURE_NUM = 10
CAPTURE_INTVAL = 5
CAMERA_READ_INTVAL = 0.1

''' ==================================================================== '''


def Info(err):
    print("face locker error: ", err)


def Error(err):
    print("face locker error: ", err)


def Fatal(err):
    print("face locker fatal: ", err)
    exit(1)


def RunFaceLocker(lock_func):
    while True:
        if not False and not CaptureFace():
            lock_func()
        time.sleep(CAPTURE_INTVAL)


def CaptureFace():
    face = False
    camera = cv2.VideoCapture(0)
    try:
        for i in range(CAPTURE_NUM):
            ret, image = camera.read()
            if not ret:
                return False
            cv2.imwrite(TMP_PIC_FILE, image)
            image = face_recognition.load_image_file(TMP_PIC_FILE)
            locations = face_recognition.face_locations(image)
            if locations:
                face = True
                break
            time.sleep(CAMERA_READ_INTVAL)
    except Exception as err:
        print("Capture image exception: ", err)
    finally:
        del camera
    return face

# get linux lock


def linux_lockcmd():
    return UBUNTU_LOCK_CMD

# get lock


def GetLockFunc():
    cmd = ""
    sys = platform.system()
    if sys == "Windows":
        cmd = WIN_LOCK_CMD
    elif sys == "Darwin":
        cmd = MAC_LOCK_CMD
    elif sys == "Linux":
        cmd = linux_lockcmd()
    else:
        Fatal("unknown system")

    def LockFunc():
        subprocess.call(cmd, shell=True)
    return LockFunc


def GetCheckFunc():
    def DarwinFunc():
        try:
            import Quartz
            status = Quartz.CGSessionCopyCurrentDictionary()
            if status:
                if status.get("CGSSessionScreenIsLocked", 0) == 1 or \
                        status.get("kCGSSessionOnConsoleKey", 1) == 0:
                    return True
            return False
        except ImportError as err:
            print("")


if __name__ == "__main__":
    RunFaceLocker(GetLockFunc())

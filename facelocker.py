#!/usr/bin/python3
import platform
import subprocess
import sys
import time

import cv2
import face_recognition

''' ==================================================================== '''
# Cross-platform
UBUNTU_LOCK_CMD = r"gnome-screensaver-command --lock"
UBUNTU_CHECK_CMD = r"gnome-screensaver-command -q"
MAC_LOCK_CMD = r"/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession \
 -suspend"

# Config
TMP_PIC_FILE = r"face.png"
CAPTURE_NUM = 10
CAPTURE_INTVAL = 5
CAMERA_READ_INTVAL = 0.1

''' ==================================================================== '''


def Error(info):
    print(info, file=sys.stderr)


def Fatal(info):
    Error(info)
    exit(1)


def RunFaceLocker(lock, check):
    while True:
        if not check() and not CaptureFace():
            lock()
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
        Error("Capture image exception: %s" % err)
    finally:
        del camera
    return face


def GetPlatformFunc():
    cmd = ""
    check = None
    system = platform.system()
    if system == "Darwin":
        cmd = MAC_LOCK_CMD

        def checkDarwin():
            import Quartz
            status = Quartz.CGSessionCopyCurrentDictionary()
            if status:
                if status.get("CGSSessionScreenIsLocked", 0) == 1 or \
                        status.get("kCGSSessionOnConsoleKey", 1) == 0:
                    return True
            return False

        check = checkDarwin
    elif system == "Linux":
        cmd = UBUNTU_LOCK_CMD

        def checkLinux():
            return subprocess.getoutput(UBUNTU_CHECK_CMD).split()[-1] == "active"

        check = checkLinux
    elif system == "Windows":
        Fatal("windows not support yet")
    else:
        Fatal("unknown system")
        exit(1)

    def lock():
        return subprocess.call(cmd, shell=True)
    return lock, check


if __name__ == "__main__":
    lock, check = GetPlatformFunc()
    RunFaceLocker(lock, check)

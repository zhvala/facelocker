import subprocess

import cv2
import face_recognition


camera = cv2.VideoCapture(0)
i = 0
while i < 10:
    return_value, image = camera.read()
    cv2.imwrite('opencv'+str(i)+'.png', image)
    i += 1
del(camera)
# Cross-platform
MAC_LOCK_CMD = r"/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend"


TEST_PIC1 = "/Users/zhvala/Pictures/face1.jpg"
TEST_PIC2 = "/Users/zhvala/Pictures/face2.jpg"
TEST_PIC3 = "/Users/zhvala/Pictures/face3.jpg"
TEST_PIC4 = "/Users/zhvala/Pictures/face4.png"
TEST_PIC5 = "opencv0.png"

image = face_recognition.load_image_file(TEST_PIC5)

face_locations = face_recognition.face_locations(image)
print(face_locations)
if len(face_locations) == 0:
    lock_cmd = MAC_LOCK_CMD
    subprocess.call(lock_cmd, shell=True)

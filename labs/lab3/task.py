import cv2 as cv
from pathlib import Path


DIR = Path(__file__).parent

# https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
# CASCADE = cv.CascadeClassifier(f'{DIR}\haarcascade_frontalface_default.xml')


def detect_face():
    imgs_dir = DIR.joinpath('photos')
    for img in imgs_dir.iterdir():
        print(img)
        current = cv.imread(str(img))
        cv.imshow('.', current)
        break

detect_face()
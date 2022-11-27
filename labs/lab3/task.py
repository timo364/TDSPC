import cv2 as cv

from pathlib import Path


# DIR = Path().absolute().joinpath(__file__).parent
DIR = Path(__file__).parent


# https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
CASCADE = cv.CascadeClassifier(f'{DIR}/haarcascade_frontalface_default.xml')


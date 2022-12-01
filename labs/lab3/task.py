import cv2 as cv

from pathlib import Path
from multiprocessing import Pool


# Defining current project working directory.
DIR = Path(__file__).parent


def detect_face_and_write_result(img: Path):
    """
    Detects faces using OpenCV's `CascadeClassifier()` class with Haar Cascade
    method. If face is detected on given image, draws a red rectangle around
    face and saving changed image to `output` directory.
    """
    # https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
    classifier = cv.CascadeClassifier(
        f'{DIR}\haarcascade_frontalface_default.xml')

    # Readting image and turning it to gray.
    curr_img = cv.imread(str(img))
    gray_img = cv.cvtColor(curr_img, cv.COLOR_BGR2GRAY)

    # More about 'scaleFactor' and 'minNeighbors':
    # https://stackoverflow.com/a/55628240
    faces_num = classifier.detectMultiScale(
        gray_img, scaleFactor=1.3, minNeighbors=7)

    # If image has one or more face(s)...
    if len(faces_num) >= 1:
        for (x, y, w, h) in faces_num:
            # ...draw red rectangle around face...
            cv.rectangle(
                curr_img, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)

        # ...and save new image to 'output' directory.
        new_file_path = str(DIR.joinpath('output') / img.name)
        cv.imwrite(new_file_path, curr_img)


if __name__ == '__main__':
    # At every start, create 'output' directory if not exists,
    # and wipe everyting in it.
    out_dir = DIR.joinpath('output')
    out_dir.mkdir(parents=True, exist_ok=True)
    [f.unlink() for f in out_dir.iterdir()]

    # Define directory with images and how many of them are there.
    imgs_dir = DIR.joinpath('photos')
    imgs_count = len([i for i in imgs_dir.iterdir()])

    # Creating a Pool, specifying number of processes will be created with
    # images count.
    pool = Pool(imgs_count)

    # For every image...
    for img in imgs_dir.iterdir():
        # ...create a asynchronus worker (process) and start task.
        pool.apply_async(detect_face_and_write_result, (img,))

    # Closing all workers (processes) and waiting for finishing everyting.
    pool.close()
    pool.join()
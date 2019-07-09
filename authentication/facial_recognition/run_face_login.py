import cv2
from facial_recognition import FaceRecogniser
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # Face recogniser object
    face_recogniser = FaceRecogniser()

    # Get camera instance
    camera = cv2.VideoCapture(2)

    # Input key to capture image or quit
    key = input('Press ENTER to capture image, c to cancel: ')
    if key == 'c':
        exit()

    # Capture one image from camera
    ret, image = camera.read()
    plt.imshow(image)
    plt.show()
    print(face_recogniser.recognise_face(img=image, path=False))
    camera.release()

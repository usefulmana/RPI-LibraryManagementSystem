import cv2
import os


def take_pictures(email):
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("register")
    img_counter = 0
    name = email[:-10]
    folder = "/home/pi/Desktop/authentication/classic-login/images/{}".format(name)
    if not os.path.exists(folder):
        os.makedirs(folder)

    while True:
        ret, frame = cam.read()
        cv2.imshow("register", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

        elif k % 256 == 32:
            # SPACE pressed
            img_name = "{}/{}.jpg".format(folder, img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

        if img_counter == 3:
            break

    cam.release()
    cv2.destroyAllWindows()


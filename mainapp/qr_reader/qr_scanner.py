# USAGE
# python3 barcode_scanner_console.py

## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
## pip3 install pyzbar

# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
from qr_reader.qr_parser import QRParser
import datetime
import imutils
import time
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import cv2


class QRScanner:
    _instance = None

    # Only one instance of this class should exist
    @staticmethod
    def get_instance():
        """
         This method will return an instance of QRScanner class
        :return:  An instance of QRScanner class
        """
        if QRScanner._instance is None:
            QRScanner()
        return QRScanner._instance

    def __init__(self):
        if QRScanner._instance is not None:
            raise Exception("This class is singleton")
        else:
            QRScanner._instance = self

    @staticmethod
    def scan_qr():
        """
        Activate the camera and scan for QR code
        :return: Nothing
        """
        # Give user time to prepare
        print("[INFO] starting video stream in 5...")
        qr_parser = QRParser.get_instance()
        vs = VideoStream(src=0).start()
        time.sleep(1)
        print("[INFO] starting video stream in 4...")
        time.sleep(1)
        print("[INFO] starting video stream in 3...")
        time.sleep(1)
        print("[INFO] starting video stream in 2...")
        time.sleep(1)
        print("[INFO] starting video stream in 1...")

        found = ''

        # loop over the frames from the video stream
        loop_count = 0
        # Try to scan for QR 10 times, if nothing shows up turn off camera
        while loop_count < 6:
            loop_count += 1
            # grab the frame from the threaded video stream and resize it to
            # have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)

            # loop over the detected barcodes
            for barcode in barcodes:
                # the barcode data is a bytes object so we convert it to a string
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type
                print("[FOUND] Type: {}, Data: {}".format(barcode_type, barcode_data))
                # if the barcode text has not been seen before print it and update the set
                found = barcode_data
            if qr_parser.return_book_from_QR_code(found) and found is not None:
                break
            # wait a little before scanning again

        # close the output CSV file do a bit of cleanup
        print("[INFO] Quitting...")
        time.sleep(5)
        vs.stop()


if __name__ == '__main__':
    QRScanner().get_instance().scan_qr()
# ==========================================================================
# REFERENCE: Face Recognition library from ageitgey @ Github
# https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py
# ==========================================================================

import face_recognition as FR
import cv2
import numpy as np


class FaceRecogniser:
    def __init__(self):
        self._names = []
        self._encodings = []

    def encode_face(self, img_path):
        img_file = FR.load_image_file(file=img_path)
        face_encoding = FR.face_encodings(face_image=img_file)[0]
        return face_encoding

    def recognise_face(self, img_path):
        image_file = FR.load_image_file(file=img_path)

        try:
            # Find location of the face in image and get its encoding
            face_encoding = FR.face_encodings(face_image=image_file)[0]

            # Find face match from list of known faces
            matches = FR.compare_faces(known_face_encodings=self._encodings,
                                       face_encoding_to_check=face_encoding)

            # If no face matches found, return 'Unknown'
            if not True in matches:
                return 'Unknown'

            # If face matches are found
            else:
                # If only 1 match is found, return the person's name
                if matches.count(True) == 1:
                    name = self._names.index(matches.index(True))

                # If more than 1 match is found, return the face with minimum distance
                else:
                    face_distances = FR.face_distance(face_encodings=self._encodings,
                                                      face_to_compare=face_encoding)
                    best_match_index = int(np.argmin(face_distances))
                    name = self._names[best_match_index]

                return name

        except IndexError:
            print('--FaceRecognitionErr: No face detected in given image.')
            quit()

    def load_face_encodings(self):
        pass
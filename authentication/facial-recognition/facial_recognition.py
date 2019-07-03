# ==========================================================================
# REFERENCE: Face Recognition library from ageitgey @ Github
# https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py
# ==========================================================================

import face_recognition as FR
import numpy as np
from face_encoding import FaceEncoding


class FaceRecogniser:
    def __init__(self):
        self._names = []
        self._encodings = []

    def recognise_face(self, img_path):
        """
            Check if the person in image is within the member database
            using face recognition
        :param img_path: path to image of face
        :return: name/user ID of the person if existing in database, else 'Unknown'
        """
        # Get face encoding from image
        face_encoding = FaceEncoding.encode_face(img_path=img_path)

        # Find face match from list of known faces
        matches = FR.compare_faces(known_face_encodings=self._encodings,
                                   face_encoding_to_check=face_encoding)

        # If no face matches found, return 'Unknown'
        if True not in matches:
            return 'Unknown'

        # If face matches are found
        else:
            # If only 1 match is found, return the person's name
            if matches.count(True) == 1:
                name = self._names[matches.index(True)]

            # If more than 1 match is found, return the face with minimum distance
            else:
                face_distances = FR.face_distance(face_encodings=self._encodings,
                                                  face_to_compare=face_encoding)
                best_match_index = int(np.argmin(face_distances))
                name = self._names[best_match_index]

            return name

    def load_face_encodings(self):
        pass


if __name__ == '__main__':
    face_recogniser = FaceRecogniser()
    print(face_recogniser.recognise_face(img_path='imgs/obama/obama2.jpg'))

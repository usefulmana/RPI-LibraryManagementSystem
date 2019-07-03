# ==========================================================================
# REFERENCE: Face Recognition library from ageitgey @ Github
# https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py
# ==========================================================================

import face_recognition as FR
import numpy as np
import pandas as pd
import os
from face_encoding import FaceEncoder


class FaceRecogniser:
    def __init__(self):
        self._names = []
        self._encodings = []
        self.load_face_encodings()

    def recognise_face(self, img_path):
        """
            Check if the person in image is within the member database
            using face recognition
        :param img_path: path to image of face
        :return: name/user ID of the person if existing in database, else 'Unknown'
        """
        # Get face encoding from image
        face_encoding = FaceEncoder.encode_face(img_path=img_path)

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
        """
            Load information including person's name and face encoding from CSV file
        :return: Class properties '_names' and '_encodings' are updated, data summary is printed
        """
        # Load data from CSV file
        faces_df = pd.read_csv('face_db.csv')

        # Save list of names to class property
        self._names = faces_df['name']

        # Save list of face encodings to class property
        for encoding_str in faces_df['encodings']:
            # Remove newline characters and brackets
            encoding_split = encoding_str.replace('\n', '')[1:-1].split()
            encoding_float = [float(x) for x in encoding_split]
            self._encodings.append(encoding_float)

        # Print out data summary
        print('Database contains {} people'.format(len(self._names)))


if __name__ == '__main__':
    face_recogniser = FaceRecogniser()

    # Test with data from test folder
    file_names = os.listdir(path='imgs/test/')
    for file_name in file_names:
        recognised = face_recogniser.recognise_face('imgs/test/{}'.format(file_name))
        print('Ground truth: {} - Recognised: {}'.format(file_name, recognised))

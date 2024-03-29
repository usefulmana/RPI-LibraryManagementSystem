# ==========================================================================
# REFERENCE: Face Recognition library from ageitgey @ Github
# https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py
# ==========================================================================

import face_recognition as FR
import numpy as np
import pandas as pd
from face_encoding import FaceEncoder


class FaceRecogniser:
    def __init__(self):
        self._names, self._encodings = self.load_face_encodings()
        self.load_face_encodings()

        # Print out data summary
        print('Database contains {} people'.format(len(self._names)))

    def recognise_face(self, img, path=True):
        """
            Check if the person in image is within the member database
            using face recognition
        :param img: input image or path to image
        :param path: boolean whether input an image file or path to image file
        :return: name/user ID of the person if existing in database, else 'Unknown'
        """
        # Get face encoding from image
        face_encoding = FaceEncoder.encode_face(img=img, path=path)

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

    @staticmethod
    def load_face_encodings():
        """
            Load information including person's name and face encoding from CSV file
        :return: lists of names and face encodings
        """
        # Load data from CSV file
        faces_df = pd.read_csv('face_db.csv')

        # Save list of names to class property
        names = faces_df['name']
        encodings = []

        # Save list of face encodings to class property
        for encoding_str in faces_df['encodings']:
            # Remove newline characters and brackets
            encoding_split = encoding_str.replace('\n', '')[1:-1].split()
            encoding_float = [float(x) for x in encoding_split]
            encodings.append(encoding_float)

        return names, encodings


# if __name__ == '__main__':
#     face_recogniser = FaceRecogniser()
#
#     # Test with data from test folder
#     file_names = os.listdir(path='imgs/test/')
#     for file_name in file_names:
#         recognised = face_recogniser.recognise_face('imgs/test/{}'.format(file_name))
#         print('Ground truth: {} - Recognised: {}'.format(file_name, recognised))

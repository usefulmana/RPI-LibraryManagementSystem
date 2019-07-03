import face_recognition as FR
import pandas as pd
import os


class FaceEncoder:
    def __init__(self):
        # Initalise dataframe to store name, paths and encodings
        self._faces_df = pd.DataFrame(columns=['name', 'img_path', 'encodings'])

    @staticmethod
    def encode_face(img_path):
        """
            Get encoding of the face in the given image
        :param img_path: path to image of face
        :return: encoding of face in image, if no face found, raise error and finish
        """
        try:
            img_file = FR.load_image_file(file=img_path)
            face_encoding = FR.face_encodings(face_image=img_file)[0]
            return face_encoding
        except IndexError:
            print('--FaceRecognitionErr: No face detected in given image.')
            quit()

    def load_data(self):
        """
            Fetch all images from "known" directory to dataframe
            and encode each one of them
        """
        # Get all image file names
        file_names = os.listdir(path='imgs/train/')

        # Load names and image paths to faces dataframe
        self._faces_df['name'] = [x.split('.')[0] for x in file_names]
        self._faces_df['img_path'] = ['imgs/train/{}'.format(x) for x in file_names]

        # Iterate through faces dataframe and get face encoding
        for index, row in self._faces_df.iterrows():
            print('Encoding image', index)
            row['encodings'] = self.encode_face(row['img_path'])

    def save_as_csv(self):
        """
            Save generated known faces dataframe as CSV file
        :return: None, but face_db.csv file is created in the same directory
        """
        self._faces_df.to_csv('face_db.csv', index=False)

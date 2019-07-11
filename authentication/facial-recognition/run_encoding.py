from face_encoding import FaceEncoder


if __name__ == '__main__':
    face_encoder = FaceEncoder()
    face_encoder.load_data()
    face_encoder.save_as_csv()

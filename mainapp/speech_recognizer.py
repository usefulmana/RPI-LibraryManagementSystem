import speech_recognition as sr
import subprocess
import time


class SpeechRecognizer:
    """
    This method will return an instance of SpeechRecognizer class
   :return:  An instance of SpeechRecognizer class
   """
    _instance = None

    @staticmethod
    def get_instance():
        if SpeechRecognizer._instance is None:
            SpeechRecognizer()
        return SpeechRecognizer._instance

    def __init__(self):
        if SpeechRecognizer._instance is not None:
            raise Exception("This class is singleton")
        else:
            SpeechRecognizer._instance = self
            self._MIC = "Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)"

    # Set the device ID of the mic that we specifically want to use to avoid ambiguity
    def get_device_id(self):
        device_id = ''
        for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
            if (microphone_name == self._MIC):
                device_id = i
                break
        return device_id

    def record_and_decipher_audio(self):
        # obtain audio from the microphone
        device_id = SpeechRecognizer.get_instance().get_device_id()
        r = sr.Recognizer()
        with sr.Microphone(device_index=device_id) as source:
            # clear console of errors
            subprocess.run("clear")

            # wait for a second to let the recognizer adjust the
            # energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source)

            print("Say a book's name or an author... ")
            print("Mic open in 3... ")
            time.sleep(1)
            print("Mic open in 2... ")
            time.sleep(1)
            print("Mic open in 1... ")
            print("Begin")
            try:
                audio = r.listen(source, timeout=1.5)
            except sr.WaitTimeoutError:
                print("Listening timed out whilst waiting for phrase to start")
                quit()
            # recognize speech using Google Speech Recognition
            try:
                text = r.recognize_google(audio_data=audio, language='us-EN')
                print("You said '{}'".format(text))
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

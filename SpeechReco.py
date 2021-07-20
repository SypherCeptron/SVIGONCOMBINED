import speech_recognition as sr
import pyttsx3
import time


def recognize_speech_from_mic(recognizer, microphone):


    # adjust the recognizer sensitivity to ambient noise and record audio from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }


    try
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


# working of user's command listener
def SpeechReco():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    start = time.time()

    while 1:

        SpeechText = recognize_speech_from_mic(recognizer, microphone)
        if SpeechText["transcription"]:
            break
        engine = pyttsx3.init()
        engine.say("I didn't catch that. What did you say?")
        engine.runAndWait()
        stop = time.time()
        if int(stop - start) > 10:
            engine = pyttsx3.init()
            engine.say("I am going back to sleep")
            engine.runAndWait()
            SilentSpeechReco()

    return SpeechText["transcription"]


# working of keyword tracker
def SilentSpeechReco():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while 1:

        SpeechText = recognize_speech_from_mic(recognizer, microphone)
        if SpeechText["transcription"] == "hello":
            engine = pyttsx3.init()
            engine.say("hello")
            engine.runAndWait()

            return
        if SpeechText["transcription"] == "stop":
            engine = pyttsx3.init()
            engine.say("I am shutting down")
            engine.runAndWait()
            exit()

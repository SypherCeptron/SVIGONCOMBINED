import cv2
import pyttsx3
from time import time
from BFT import BFT
from ColorReco import ColorReco
from SpeechReco import SpeechReco,SilentSpeechReco
import datetime
from ObjectDetector import ObjectDetector
from OCR import OCR
from Currency import Currency
def Redirector(x):
    #Gets the best fram
    frame = BFT()
    #module selections
    if(x == 1): Aud = ColorReco(frame)
    if(x == 2): Aud = OCR(frame)
    if(x == 3):
                Aud = ObjectDetector(frame)
                if len(Aud) == 0:Aud = "No Objects nearby"
                if len(Aud) == 1:Aud = "There is a "+str(Aud)+" front of you"
                else:
                    A = Aud.pop(len(Aud)-1)
                    B = ", ".join(Aud)
                    Aud = "There are  "+str(Aud)+" and "+str(A) +" in front of you"
    if(x == 4):Aud = "you are holding" + currency(frame) + "Rupees"


    #coverting text into voice
    engine = pyttsx3.init()
    engine.say(Aud)
    engine.runAndWait()
    ActiveListener()



def ActiveListener():
    start = time()

    while (1):
        #listning to User's to user cammands
        Transcription = SpeechReco()
        if Transcription == "time":
            engine = pyttsx3.init()
            #getting todays date and time
            x = datetime.datetime.now()
            DateTime = x.strftime("Time at present is %H %M %S")
            engine.say(DateTime)
            engine.runAndWait()
            ActiveListener()
            break
        if Transcription == "date":
            engine = pyttsx3.init()
            #getting todays date and time
            x = datetime.datetime.now()
            DateTime = x.strftime("Today's date is %A %d %B %Y")
            engine.say(DateTime)
            engine.runAndWait()
            ActiveListener()
            break
        if Transcription == "colour":
            Redirector(1)
            break
        if Transcription == "text":
            Redirector(2)
        if Transcription == "object":
            Redirector(3)
        if Transcription == "currency":
            Redirector(4)
            break
        #incase of invalid commands
        if Transcription != "time" or Transcription != "color" or Transcription != "object" or Transcription != "currency" or Transcription != "text" or Transcription != "sleep":
            engine = pyttsx3.init()
            engine.say("Can you please repeat")
            engine.runAndWait()
        #putting back to silentlistner manually
        if Transcription == "sleep":
            engine = pyttsx3.init()
            engine.say("I am going back to sleep")
            engine.runAndWait()
            Silentlistener()
        stop = time()
        #incase the user leaves the device on
        if int(stop-start) > 10:
            engine = pyttsx3.init()
            engine.say("I am going back to sleep")
            engine.runAndWait()
            Silentlistener()
#Voice activation/keyword

def Silentlistener():
    SilentSpeechReco()
    engine = pyttsx3.init()
    engine.say("Ask me something")
    engine.runAndWait()
    ActiveListener()
#Main initializer
Silentlistener()



import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()

def Speak(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

while True:
    with sr.Microphone() as source:
        print("Say something:")
        r.adjust_for_ambient_noise(source, duration=0.2)

        try:
            audio = r.listen(source, timeout= 3)
            text = r.recognize_google(audio)
            text = text.lower()
            print("You said:", text)
            Speak(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.WaitTimeoutError as w:
            print(f"{w}; Please Speak Up!")
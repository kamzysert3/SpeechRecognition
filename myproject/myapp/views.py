from django.shortcuts import render
from django.http import JsonResponse
import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()

def index(request):
    return render(request, 'myapp/index.html')

def Speak(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def get_audio(request):
    if request.method == 'POST':
        Speak("hello, i'm axl your personal translator")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            try:
                audio = r.listen(source, timeout=5)
                text = r.recognize_google(audio).lower()
                return JsonResponse({'text': text})
            except sr.UnknownValueError:
                return JsonResponse({'error': 'Google Speech Recognition could not understand audio'})
            except sr.RequestError as e:
                return JsonResponse({'error': f'Could not request results from Google Speech Recognition service; {e}'})
            except sr.WaitTimeoutError as w:
                return JsonResponse({'error': f'{w}; Please Speak Up!'})

    return JsonResponse({'error': 'Invalid request method.'})

from django.shortcuts import render
from django.http import JsonResponse
import speech_recognition as sr
import pyttsx3
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import re

r = sr.Recognizer()
name = ''

def index(request):
    return render(request, 'myapp/index.html')

def Speak(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def UserRecognition():
    global name
    Speak("Hello, What is your name")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        try:
            audio1 = r.listen(source, timeout=3)
            name = r.recognize_google(audio1).lower()
            Speak(f"How are you {name}")
            return {'text': name}
        except sr.UnknownValueError:
            return {'error': 'Google Speech Recognition could not understand audio'}
        except sr.RequestError as e:
            return {'error': f'Could not request results from Google Speech Recognition service; {e}'}
        except sr.WaitTimeoutError as w:
            return {'error': f'{w}; Please Speak Up!'}


def recognize_integer(sentence):
    matches = re.findall(r'\b\d+\b', sentence)
    number = int(matches[0]) if matches else None
    return number


def decrease_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        current_volume = volume.GetMasterVolumeLevelScalar()

        new_volume = max(0.0, current_volume - 0.15)

        volume.SetMasterVolumeLevelScalar(new_volume, None)

        return JsonResponse({'success': True, 'new_volume': new_volume})
    except Exception as e:
        return JsonResponse({'error': f'Error adjusting volume: {e}'})



def increase_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        current_volume = volume.GetMasterVolumeLevelScalar()

        new_volume = min(1.0, current_volume + 0.15)

        volume.SetMasterVolumeLevelScalar(new_volume, None)
        return JsonResponse({'success': True, 'new_volume': new_volume})

    except Exception as e:
        return JsonResponse({'error': f'Error adjusting volume: {e}'})


def affect_volume(number):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, min(1.0, current_volume + number))

    volume.SetMasterVolumeLevelScalar(new_volume, None)

def get_audio(request):
    global name
    if request.method == 'POST':
        if name:
            Speak(f"Hello {name}, What can I do for you")
        else:
            Speak("Hello, I'm Axl, your personal Assistant, What can I do for you")     
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            try:
                audio = r.listen(source, timeout=5)
                text = r.recognize_google(audio).lower()
                if 'hello' in text or 'hi' in text or 'hey' in text:
                    UserRecognition()
                if 'increase' and 'volume' in text:
                    increase_volume()
                if ('reduce' in text or 'decrease' in text) and 'volume' in text:
                    decrease_volume()
                return JsonResponse({'text': text})
            except sr.UnknownValueError:
                return JsonResponse({'error': 'Google Speech Recognition could not understand audio'})
            except sr.RequestError as e:
                return JsonResponse({'error': f'Could not request results from Google Speech Recognition service; {e}'})
            except sr.WaitTimeoutError as w:
                return JsonResponse({'error': f'{w}; Please Speak Up!'})
    return JsonResponse({'error': 'Invalid request method.'})

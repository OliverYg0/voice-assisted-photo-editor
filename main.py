import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageEnhance
import re

active = True
root = tk.Tk()
root.withdraw()
EXT_WRDS = ['stop', 'bye', 'goodbye', 'finished']
SEARCH_TERMS = ['find', 'search', 'open', 'image', 'get', 'select', 'photo']
CLOSE_WORDS = ['close', 'remove', 'new']
r = sr.Recognizer()
print('[STATUS: Active] Currently listning...')
directory = ''
image = None
edited = False

def get_factors(command):
    if len([int(i) for i in re.findall(r'\b\d+\b', command)]) > 0:
        return [int(i) for i in re.findall(r'\b\d+\b', command)]
    else:
        return 0

def clean_factor(command, factor):
    if '-' in command or 'deacr1ease' in command or 'negertive' in command:
        factor =  factor * -1
    
    factor = float(factor)

    return factor
    
def adjust_brightness(img, factor):
    print('Brightness adjusted by:', factor)
    edit = ImageEnhance.Brightness(img)
    return edit.enhance(factor)

def adjust_sharpness(img, factor):
    print('Sharpness adjusted by:', factor)
    edit = ImageEnhance.Sharpness(img)
    return edit.enhance(factor)

def adjust_contrast(img, factor):
    print('Contrast adjusted by:', factor)
    edit = ImageEnhance.Contrast(factor)
    return edit.enhance(factor)

while active:
    change_log = 0
    with sr.Microphone() as source:
        audio = r.listen(source)

        try:
            command = r.recognize_google(audio).lower().strip()
            print('\nCommand:', command)

            for word in EXT_WRDS:
                if word in command.lower():
                    active = False

            for word in SEARCH_TERMS:
                if word in command:
                    if image == None:
                        directory = filedialog.askopenfilename()
                        print('Image:', directory)
                        image = Image.open(directory)

            for word in CLOSE_WORDS:
                if word in command:
                    if image != None:
                        directory = ''
                        image = None
                        edited = False
                        print('Image closed.')

            if image != None:
                if 'brightness' in command:
                    factor = clean_factor(command, get_factors(command)[change_log])
                    image = adjust_brightness(image, factor)
                    edited = True
                    change_log += 1

                if 'sharpness' in command:
                    factor = clean_factor(command, get_factors(command)[change_log])
                    image = adjust_sharpness(image, factor)
                    edited = True
                    change_log += 1

                if 'contrast' in command:
                    factor = clean_factor(command, get_factors(command)[change_log])
                    image = adjust_contrast(image, factor)
                    edited = True
                    change_log += 1

                if 'show' in command:
                    image.show()

                if 'save' in command:
                    if edited:
                        image.save(directory)
                        print('Image saved.')
        except:
            pass

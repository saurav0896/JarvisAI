import pyttsx3
import speech_recognition as sr
import datetime
import os
import sys
import cv2
import random
import wikipedia
import webbrowser
import requests
import time
import pyautogui
import pywhatkit as kit
from requests import get
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisUI import Ui_jarvisUI   # Importing our UI Python file


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


# text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# wish function
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour <=12:
        speak('Good Morning')
    elif hour >= 12 and hour <=18:
        speak('Good Afternoon')
    else:
        speak('Good Evening')

    speak('I am Jarvis Sir, Please tell me how can I help you')


# fetch latest news
def news():
    url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apikey=45f2cca00ac74a5ead8bc9af6982eb4e'
    main_page = requests.get(url).json()
    articles = main_page['articles']
    head = []
    days = ['first', 'second', 'third', 'forth', 'fifth', 'sixth', 'seventh', 'eight', 'ninth', 'tenth']
    for ar in articles:
        head.append(ar['title'])
    for i in range(len(days)):
        speak(f"today's {days[i]} news is : {head[i]}")


# fetch location
def location():
    try:
        ipAdd = requests.get('https://api.ipify.org').text
        url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
        geo_request = requests.get(url)
        geo_data = geo_request.json()

        city = geo_data['city']
        country = geo_data['country']
        speak(f"Sir I am not sure, but I think we are in {city} city of country {country}")

    except Exception as e:
        speak("Sorry Sir,due to network issue I am not able to fetch the location")
        pass


# Adding UI with backend
class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    # User Command
    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            r.pause_threshold = 1
            audio = r.listen(source, timeout=1, phrase_time_limit=5)

        try:
            print('Recongnizing....')
            query = r.recognize_google(audio, language='en-in')
            print(f'User Said: {query}')

        except Exception as e:
            speak('Say that again please')
            return 'none'
        return query

    def TaskExecution(self):
        wish()
        while True:
            self.query = self.takecommand().lower()
            if 'jarvis' in self.query:
                self.query = self.query.replace('jarvis', '')

            # building logic for commands
            if 'open notepad' in self.query:
                npath = "C:\\WINDOWS\\system32\\notepad.exe"
                os.startfile(npath)

            elif 'close notepad' in self.query:
                speak('Closing notepad sir')
                os.system('taskkill /f /im notepad.exe')

            elif 'open command prompt' in self.query:
                os.system('start cmd')

            elif 'open camera' in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k ==27:
                        break
                cap.release()
                cv2.destroyAllWindows()

            elif 'play music' in self.query:
                mpath = "E:\\music"
                songs = os.listdir(mpath)
                # rd = random.choice(songs)
                for song in songs:
                    if song.endswith('.mp3'):
                        os.startfile(os.path.join(mpath, song))

            elif 'ip address' in self.query:
                ip = get('https://api.ipify.org').text
                speak(f'Your IP Address is {ip}')

            elif 'who is' in self.query:
                wiki = self.query.replace('who is ', '')
                speak('Searching Wikipedia')
                wikiresult = wikipedia.summary(wiki, sentences=1)
                speak('According to wikipedia')
                speak(wikiresult)
                print(wikiresult)

            elif 'on browser' in self.query:
                srv = self.query.replace('on browser', '')
                srv = srv.replace('open', '')
                webbrowser.open(srv + '.com')

            elif 'open google' in self.query:
                speak('sir what you want me to search on google')
                cm = self.takecommand().lower()
                webbrowser.open(f'{cm}')

            elif 'play song ' in self.query:
                artist = self.query.replace('play', '')
                kit.playonyt(artist)

            elif 'latest news' in self.query:
                speak('Please wait, fetching latest news')
                news()

            elif 'location' in self.query:
                speak('Wait sir, let me check sir')
                location()

            elif 'take screenshot' in self.query:
                speak('Sir please tell me the name of screenshot file')
                filename = self.takecommand().lower()
                speak('Sir please hold the screen, taking screenshot')
                time.sleep(3)
                ssimg = pyautogui.screenshot()
                ssimg.save(f'{filename}.png')
                speak(f'Sir screenshot is saved to main folder with name {filename}')

            elif 'shutdown' in self.query:
                speak('Thanks for using me sir, have a good day')
                sys.exit()


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_jarvisUI()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("D:/PythonProjects/JARVIS/lib/Bg.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/PythonProjects/JARVIS/lib/loader.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        lable_time = current_time.toString('hh:mm:ss')
        lable_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(lable_time)
        print(lable_date)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())


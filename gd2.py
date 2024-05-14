import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random
import stats


engine = pyttsx3.init('sapi5') 
voices = engine.getProperty('voices') 
engine.setProperty('rate', 175)     
engine.setProperty('voice', voices[1].id) 

dic= {'REC1' : 'RECIEVER1@gmail.com',
      'REC2': 'RECIEVER2@gmail.com'}

def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wishMe(name):
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!"+name)

    elif hour>=12 and hour<18:
        speak("Good Afternoon!"+name)

    else:
        speak("Good Evening! "+name)
    speak("Hello panel members, virtual desktop assistant here , How may I help You?")
    

def sendEmail(to, content):
    try :
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        sender_email = 'SENDER_EMAIL@gmail.com'
        sender_pass = ''
        to_list = to.split(' ')
        server.login(sender_email, sender_pass)
        for name in to_list:
            if name.lower() in dic.keys():
                recipient_email = dic.get(name.lower())
                server.sendmail(sender_email, recipient_email, content)
        server.close()
    except Exception as e:
        print('Exception',e)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I'm Listening...")
        r.energy_threshold=800
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        speak("Okay! ")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        speak("Say that again please...")
        return takeCommand()
    return query


def listenCommand():
    while True:
        query = takeCommand().lower()
        # web_browser_path= "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s"
        web_browser_path= "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"
        # web_browser_path="C:\ProgramData\Microsoft\Windows\Start Menu\Programs/Microsoft edge.exe %s"
        
        if "ok thank you" in query:
            speak("Its my pleasure sir, have a nice day")
            exit()
        
        if 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open college website' in query:
            webbrowser.open("www.gndec.ac.in")

        elif 'open department website' in query:
            webbrowser.open("cse.gndec.ac.in")
        
        elif 'give system stats' in query:
            sys_info = stats.system_stats()
            print(sys_info)
            speak(sys_info)

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open w3schools' in query:
            webbrowser.open("w3schools.com")
            

        elif 'the weather' in query:
            webbrowser.open("https://www.google.com/search?q=weather")

        elif 'open notepad' in query:
            os.system('notepad')

        elif 'open calculator' in query:
            os.system('start Calculator:')

        # elif 'open edge' in query:
        #     codePath = ""
        #     os.startfile(codePath)

        # elif 'open gallery' in query:
        #     codePath = "Pictures"
        #     os.startfile(codePath)
        
        elif 'play music' in query:
            music_dir = 'D://Songs'
            songs = os.listdir(music_dir)
            randomsongs = random.choice(songs)
            os.startfile(os.path.join(music_dir, randomsongs))
        # elif 'play music' in query:
        #  music_dir= 'D:\\Songs'      
        #  songs= os.listdir(music_dir)   
        #  print(songs)
        #  os.startfile(os.path.join(music_dir, songs[0]))  
        
        elif query.startswith('google'):
            speak('Searching google...')
            query1 = query.replace("google ", "")
            query2 = query1.replace(" ","+")
            webbrowser.open(f"https://www.google.com/search?q={query2}")

        elif query.startswith('youtube'):
            speak('Searching YouTube...')
            query1 = query.replace("youtube ", "")
            query2 = query1.replace(" ","+")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query2}")

        elif query.startswith('wikipedia'):
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif query.startswith('translate'):
            query1 = query.replace(" ","+")
            webbrowser.open(f"https://www.google.com/search?q={query1}")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'date and time' in query:
            strDate = datetime.datetime.now.strftime("%m/%d/%Y, %H:%M:%S")
            speak(f"Sir, the date and time is {strDate}")
            
        elif 'send email to' in query:
            try:
                speak("To whom? ")
                to = takeCommand()
                while not to:
                    print('Can you please say that again!')
                    to = takeCommand()
                speak("What should I say?")
                content = takeCommand()
                print (content)
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry! I am not able to send this email")
            
        elif "none" in query:
            continue
        else:
            speak('I\'m not aware,')
            cmd = takeCommand()
            if "yes" in cmd:
                speak('Googling'+query)
                query2 = query.replace(" ", "+")
                webbrowser.get(web_browser_path).open(f"https://www.google.com/search?q={query2}")
        speak("Anything else? ")


if __name__ == '__main__':
    wishMe("")
    listenCommand()

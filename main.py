
import speech_recognition as sr
import pyttsx3 as pyt
import datetime
import os
import re

import python_weather

import asyncio
import os
import geocoder



 # Initialize the speech recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine with a specific voice
engine = pyt.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'english')


pattern = r"^" + "open"

# Function to listen to user's voice command
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        # Convert speech to text
        command = r.recognize_google(audio)
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please try again.")
        return ""
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting to the speech recognition service.")
        return ""

# Function to speak the response
def speak(response):
    engine.say(response)
    engine.runAndWait()


def search_and_open_file(command):
            folder = re.split("open", command.lower())[1].strip()
            for root, dirs, files in os.walk('/'):
                for file in files:
                    if file.lower() == folder:
                        file_path = os.path.join(root, file)
                        os.system(f"xdg-open {file_path}")
                        return



async def getweather():
    # Get the current city using geolocation
    g = geocoder.ip('me')
    current_city = g.city
    
    # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        # fetch a weather forecast from the current city
        weather = await client.get(current_city)
        
        # Print the current forecast temperature
        print(f"The current forecast temperature in {current_city} is {weather.current.temperature}°C.")
        
        # Speak the current forecast temperature
        speak(f"The current forecast temperature in {current_city} is {weather.current.temperature} degrees Celsius.")
    

    
# Main loop
while True:
    command = listen()
    response = ""
    # Check if the command is to end the program
    if command.lower() == "end" or command.lower() == "stop" or command.lower() == "exit" or command.lower() == "quit" or command.lower() == "goodbye" or command.lower() == "bye":
        print("Goodbye")
        speak("Goodbye")
        break
    
    if command.lower() == "hello" or command.lower() == "hi":
        print("Hello! How can I assist you today?")
        speak("Hello! How can I assist you today?")
        
    if command.lower() == "what is your name":
        print("My name is Python Assistant.")
        speak("My name is Python Assistant.")

    if command.lower() == "what is your age":
        print("I am a computer program. I don't have an age.")
        speak("I am a computer program. I don't have an age.")

    if command.lower() == "what is the time":
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"The current time is {current_time}.")
        speak(f"The current time is {current_time}.")

    if command.lower() == "what is the weather":
        asyncio.run(getweather())

    if re.match(pattern, command.lower()):
        print("okay")
        speak("okay")
        search_and_open_file(command)
    if command.lower() == "schedule this appointment":
        print("okay")
        speak("okay")

    
    


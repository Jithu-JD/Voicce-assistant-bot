import requests
#import speech_recognition as sr

BACKEND_URL = "http://192.168.1.3:5050/api/conversation/robot_chat"

# def recognize_speech():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = r.listen(source)
#     try:
#         return r.recognize_google(audio)
#     except sr.UnknownValueError:
#         return ""
#     except sr.RequestError as e:
#         return f"Error: {e}"

def identify_face():
    # Stub: Replace with actual face recognition
    return "Lukeshwar Sahu"

def talk_to_backend(face, text):
    payload = { "face": face, "text": text }
    res = requests.post(BACKEND_URL, json=payload)
    print("Bot:", res.json().get("reply"))

if __name__ == "__main__":
    face = identify_face()
    while True:
        #user_input = recognize_speech()
        user_input = " what BIRTHDATE of mine you knew earlier "
        if user_input:
            print("You:", user_input)
            talk_to_backend(face, user_input)
        break

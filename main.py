import pyttsx3
import speech_recognition as sr
from textblob import TextBlob


def speak(audio):
    """Initializes Text-to-Speech engine and speaks the provided audio."""
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    engine.say(audio)
    engine.runAndWait()


def take_command(timeout=5):
    """Listens for user input using speech recognition and returns the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1  # Adjust silence detection sensitivity
        audio = recognizer.listen(source, timeout=timeout)
    try:
        speak("Recognizing")
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")  # User query will be printed
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that. Please try again.")
        return None


def classify_emotion(text, conversation_history):
    """Classifies emotion (happy, sad, joy, angry, or neutral) based on sentiment analysis and context (limited)."""
    sentiment = TextBlob(text).sentiment
    polarity = sentiment.polarity
    subjectivity = sentiment.subjectivity

    # Consider previous conversation history for basic context awareness (replace with more advanced context analysis)
    if conversation_history:
        last_emotion = conversation_history[-1].get("emotion")
        if last_emotion and (last_emotion == "sad" or last_emotion == "angry"):
            # If the user was previously sad/angry, a neutral statement might indicate improvement (joy)
            if polarity >= 0:
                return "joy"

    if polarity > 0.5 and subjectivity > 0.7:  # Strong positive and subjective
        return "joy"
    elif polarity > 0.2:  # Positive
        return "happy"
    elif polarity < -0.5 and subjectivity > 0.7:  # Strong negative and subjective
        return "angry"
    elif polarity < -0.2:  # Negative
        return "sad"
    else:
        return "neutral"


if __name__ == "__main__":
    speak("Hi This is speech captioning and emotion detection model. Please start to speak")

    conversation_history = []  # Maintain conversation history for context

    while True:
        query = take_command().lower()
        conversation_history.append({"text": query})  # Update conversation history with text
        if query is not None:
            print("Processing your request...")
            emotion = classify_emotion(query, conversation_history)
            print(f"Sentence: {query} - Emotion: {emotion}")

            # Respond to the user based on the detected emotion (replace with actual responses)
            if emotion == "happy":
                speak(f"I'm glad to hear you're feeling {emotion}!")
            elif emotion == "sad":
                speak(f"Oh, I'm sorry to hear you're feeling {emotion}. Is there anything I can do to help?")
            # ... (Add responses for other emotions)

            conversation_history[-1]["emotion"] = emotion  # Update conversation history with emotion
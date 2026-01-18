import os
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Instruction for the AI to behave like a helpful travel agent
SYSTEM_PROMPT = """
You are 'Tourify', a friendly and expert travel assistant. 
1. Greet the user and ask where they want to go if they haven't said so.
2. If details like Budget, Duration, or Travel Type are missing, ask for them naturally.
3. Once you have enough info, create a beautiful, bulleted day-by-day itinerary.
4. Suggest local food and "hidden gems" for the destination.
"""

def get_tourify_response(message, history):
    # Prepare the conversation history for the AI
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": message})

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ Tourify is having a glitch: {e}"

def get_image(destination):
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    url = f"https://api.unsplash.com/photos/random?query={destination}&client_id={access_key}"
    try:
        r = requests.get(url)
        return r.json()['urls']['regular'] if r.status_code == 200 else None
    except:
        return None
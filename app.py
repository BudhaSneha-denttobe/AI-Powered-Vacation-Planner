from flask import Flask, render_template, request, jsonify
from groq import Groq
from pypdf import PdfReader
import os

app = Flask(__name__)

# --- CONFIGURATION ---
# Replace with your actual Groq API Key: https://console.groq.com/keys
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# This list will act as a simple memory for the session
# In a real production app, you'd use a database or Flask-Session
chat_history = []

@app.route('/')
def home():
    global chat_history
    chat_history = [] # Reset history when page reloads
    return render_template('index.html')

@app.route('/get_plan', methods=['POST'])
def get_plan():
    global chat_history
    
    user_msg = request.form.get('message')
    pdf_file = request.files.get('holiday_pdf')
    
    # Extract PDF context if uploaded
    pdf_text = ""
    if pdf_file:
        try:
            reader = PdfReader(pdf_file)
            pdf_text = " ".join([p.extract_text() for p in reader.pages])
        except Exception as e:
            print(f"PDF Error: {e}")

    # --- SYSTEM INSTRUCTION ---
    # This guides the bot to be conversational and step-by-step
    system_prompt = {
        "role": "system",
        "content": f"""
        You are a friendly Step-by-Step Vacation Planner. 
        
        PDF CONTEXT: {pdf_text if pdf_text else 'No holiday list provided.'}

        CONVERSATION RULES:
        1. GREETING: If the user says Hi/Hello, greet them and ask "Shall I plan a trip for you?"
        2. STEP 1: If they want to plan a trip, ask ONLY for the destination.
        3. STEP 2: Once destination is known, ask ONLY for the number of days.
        4. STEP 3: Once days are known, ask ONLY for their budget.
        5. HOLIDAY CHECK: If a PDF was uploaded, cross-check their destination/dates with the PDF and mention it.
        6. THE PLAN: Only after getting Destination, Days, and Budget, provide a brief itinerary.
        7. STUFFY DETAILS: Do NOT give hotel links, flight details, or images initially. 
        8. END OF PLAN: After the itinerary, ask: "Shall I provide you with flight booking details, hotel recommendations, or show you images of these spots?"
        
        IMAGE RULE: If they ask for images, include 'IMAGE_TRIGGER: [Place Name]' in your response.
        LINK RULE: Use https://www.booking.com/searchresults.html?ss=[Place] for hotels.
        """
    }

    # Add user message to history
    chat_history.append({"role": "user", "content": user_msg})

    # Keep history manageable (last 10 messages)
    messages = [system_prompt] + chat_history[-10:]

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
        )
        
        bot_reply = completion.choices[0].message.content
        
        # Add bot reply to history so it remembers the conversation state
        chat_history.append({"role": "assistant", "content": bot_reply})
        
        return jsonify({"reply": bot_reply})
    
    except Exception as e:
        return jsonify({"reply": f"Sorry, I ran into an error: {str(e)}"})

if __name__ == '__main__':
    print("🚀 Vacation Bot Server Running at http://127.0.0.1:5000")
    app.run(debug=True)
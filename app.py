import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Gemini Setup - Aakhri aur Sahi Tarika
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Model ka naam ekdum sahi format mein (gemini-1.5-flash)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return "Hugli AI Backend is Live!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"reply": "Kuch likho bhai!"}), 400

        # AI Response
        response = model.generate_content(user_message)
        
        # Check agar response mein text hai
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "AI ne koi jawab nahi diya, fir se try karo."})

    except Exception as e:
        print(f"Error: {str(e)}")
        # Error message ko short rakha hai taaki screen par ganda na dikhe
        return jsonify({"reply": "Server Error: " + str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

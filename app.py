import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# CORS enable karne se GitHub Pages ko Render se baat karne ki permission mil jayegi
CORS(app)

# Render ki 'Environment Variables' se API Key uthana
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Gemini Model Setup
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    return "Hugli AI Backend is Running!"

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    # OPTIONS request ko handle karna (Browser security ke liye)
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        # force=True se 415 Unsupported Media Type error khatam ho jayega
        data = request.get_json(force=True)
        user_message = data.get('message')

        if not user_message:
            return jsonify({"reply": "Bhai, kuch likho toh sahi!"}), 400

        # Gemini se response lena
        response = model.generate_content(user_message)
        
        if response and response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "Gemini ne koi jawab nahi diya."}), 500

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": f"Backend Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Render ke liye port setup
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# CORS enable karne se GitHub Pages ko Render se baat karne ki permission milti hai
CORS(app)

# Render ki 'Environment Variables' se API Key uthana
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Gemini Model Setup (Naya Version)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "Hugli AI Backend is Running!"

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    # OPTIONS request ko handle karna (Browser security ke liye)
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
        
    try:
        data = request.json
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Gemini se response lena
        response = model.generate_content(user_message)
        return jsonify({'reply': response.text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Render hamesha PORT environment variable ka use karta hai
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

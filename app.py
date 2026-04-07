from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Aapki API Key
GEMINI_API_KEY = "AIzaSyCEHCaB6GcEqp6MsBs0fPokUFP2ImL8U7Y"

@app.route('/')
def home():
    return "Hugli AI Backend is Live!"

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        response = requests.post(url, json={"contents": data.get("contents")})
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

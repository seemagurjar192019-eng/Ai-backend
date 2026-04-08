import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# API KEY Setup
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# YAHAN CHANGE HAI: Hum specifically v1.5 flash model ko direct access kar rahe hain
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

@app.route('/')
def index():
    return "Backend is Active"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        
        # Generative AI call
        response = model.generate_content(user_message)
        
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Model Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

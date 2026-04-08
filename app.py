import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# API Key Setup
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Model initialization
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def health_check():
    return "Hugli AI Backend is Online"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get("message")
        
        if not user_input:
            return jsonify({"reply": "Message khali hai bhai!"}), 400

        # AI se response mangna
        response = model.generate_content(user_input)
        
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "AI ne koi jawab nahi diya. Check API Key."})

    except Exception as e:
        # Taki screen par saaf error dikhe
        return jsonify({"reply": f"Model Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Render ke liye port setup
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

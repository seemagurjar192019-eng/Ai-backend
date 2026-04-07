import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app) # Sabse zaroori: Frontend ko permission dene ke liye

# Gemini API Setup
# Yaad rakhna Render ke 'Environment Variables' mein GEMINI_API_KEY daal dena
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return "Hugli AI Backend is Live and Running!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"reply": "Bhai, kuch toh likh!"}), 400

        # AI Response Generation
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"reply": "Backend Error: " + str(e)}), 500

if __name__ == '__main__':
    # Render hamesha port 10000 mangta hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

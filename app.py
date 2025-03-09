from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch API key from environment variables
TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")
TOGETHER_AI_URL = "https://api.together.xyz/v1/chat/completions"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        print("Request received at /generate")  
        print("Request JSON:", request.json)  

        prompt = request.json.get('prompt')
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        payload = {
            "model": "meta-llama/Llama-2-7b-chat-hf",  
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200
        }

        headers = {
            "Authorization": f"Bearer {TOGETHER_AI_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(TOGETHER_AI_URL, json=payload, headers=headers)
        response_data = response.json()

        output = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response generated")

        return jsonify({"output": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


if __name__ == '__main__':
    app.run(debug=True)

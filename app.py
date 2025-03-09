from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

TOGETHER_AI_API_KEY = "399e34cb15173b05346629f57f6daabc03d901204d255cda3249345201ed9db3"  # Replace with actual key
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
    

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/features')
def features():
    return render_template('features.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

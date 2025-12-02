from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Nastavení API klíče - vlož přímo
API_KEY = "AIzaSyBND8pkPPHo6A5F5PFy6NQFwa3RqgYfoYk"
if not API_KEY:
    print("⚠️ GEMINI_API_KEY není nastaven.")
else:
    genai.configure(api_key=API_KEY)
    print("✅ API klíč je nastaven!")

# Model - zkus různé názvy: gemini-pro, gemini-1.0-pro, gemini-1.5-flash
MODEL_NAME = 'models/gemini-2.5-flash'

@app.route('/models', methods=['GET'])
def list_models():
    if not API_KEY:
        return jsonify({'error': 'GEMINI_API_KEY není nastaven'}), 400
    try:
        url = 'https://generativelanguage.googleapis.com/v1/models'
        resp = requests.get(url, params={'key': API_KEY}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        models = []
        for m in data.get('models', []):
            models.append({
                'name': m.get('name'),
                'displayName': m.get('displayName'),
                'supportedMethods': m.get('supportedGenerationMethods', m.get('supportedMethods', []))
            })
        return jsonify({'models': models})
    except Exception as e:
        print(f"ListModels error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    if not API_KEY:
        return jsonify({'error': 'GEMINI_API_KEY není nastaven'}), 400

    data = request.json or {}
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'Zpráva je prázdná'}), 400

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(user_message)
        reply = response.text
        return jsonify({'reply': reply})
    except Exception as e:
        err = str(e)
        print(f"Chat error: {err}")
        return jsonify({'error': err}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
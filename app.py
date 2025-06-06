import os
from flask import Flask, request, jsonify, render_template
import openai

# For convenience, a placeholder key is used when the OPENAI_API_KEY
# environment variable is not defined. Replace ``sk-testkey`` with a
# real key if needed.
openai.api_key = os.environ.get('OPENAI_API_KEY', 'sk-testkey')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        reply = response.choices[0].message['content']
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

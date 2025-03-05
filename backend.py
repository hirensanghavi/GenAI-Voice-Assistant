from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Google API setup
os.environ["GOOGLE_API_KEY"] = "AIzaSyDGeScN2w40rJWzLxwjaKi0KG9S57t438U"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("models/gemini-1.5-pro")

# Global variable to store conversation history
conversation_history = []

# Voice assistant function with enhanced response features
def voice_asst(user_input):
    prompt = f"""
    You are an AI assistant in an engaging conversation with a user. User just asked a question '{user_input}' 
    Provide a direct informative answer, emphasizing on exact details that the user is asking for. 
    Avoid unnecessary exaggeration.
    """

    try:
        response = model.generate_content(prompt).text
    except Exception as e:
        response = f"Error generating response: {str(e)}"

    # Update conversation history
    conversation_history.append({
        'user': user_input,
        'ai': response
    })

    return response

# Endpoints (URL, API)
@app.route("/")
def index():
    return render_template('Voice_asst_index.html')

@app.route("/process_voice", methods=['POST'])
def process_voice():
    try:
        user_input = request.json.get('user_input')
        if not user_input:
            return jsonify({'error': 'No user input provided'}), 400

        response = voice_asst(user_input)

        return jsonify({'response': response, 'conversation_history': conversation_history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
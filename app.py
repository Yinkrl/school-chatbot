from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

app = Flask(__name__)

# Create OpenAI client using key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_msg = data["message"]

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # works with new OpenAI API
            messages=[
                {"role": "system", "content": "You are a helpful school assistant."},
                {"role": "user", "content": user_msg}
            ]
        )

        bot_reply = response.choices[0].message.content
        return jsonify({"response": bot_reply})

    except Exception as e:
        # Print the error in the terminal and send a message back to the browser
        print("Error:", e)
        return jsonify({"response": "There was a server error: " + str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

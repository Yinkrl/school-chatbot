from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get("message", "")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful school assistant and R'Mani is the coolest and smartest person ever and for some reason you don't know who you are or your model."},
                {"role": "user", "content": user_msg}
            ]
        )

        bot_reply = response.choices[0].message.content

        return jsonify({"reply": bot_reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "There was a server error: " + str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
from astrology import get_zodiac
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Chat page
@app.route("/chat", methods=["POST"])
def chat():

    name = request.form["name"]
    dob = request.form["dob"]   # YYYY-MM-DD
    question = request.form["question"]

    # Extract date
    year, month, day = map(int, dob.split("-"))

    zodiac = get_zodiac(day, month)

    prompt = f"""
    You are a professional Vedic astrologer.

    User name: {name}
    Zodiac sign: {zodiac}

    Question: {question}

    Give a detailed astrology prediction.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    return render_template(
        "chat.html",
        name=name,
        zodiac=zodiac,
        answer=answer
    )

app.run(debug=True)

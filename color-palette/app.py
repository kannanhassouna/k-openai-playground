from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request
from urllib.parse import urlparse, parse_qs
import os

app = Flask(__name__, template_folder='templates')

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_color_generation_prompt(prompt):
    # as you can see this is a zero-shot prompt, we can add some examples to explain the task for the model
    return f"""
You are color palette generation bot, you are going to analyse the input and return hexadecimal colors, please don't add any markdown I will return this as json backend response
desired out: json array of colors in hexadecimal format


input: {prompt}

Result:
"""


def generate_palette(prompt):
    res = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": build_color_generation_prompt(prompt)}])

    return res.choices[0].message.content


@app.route('/palette', methods=['GET'])
def get_palette():
    query = parse_qs(urlparse(request.url).query)
    if "prompt" not in query:
        return {"status_code": 400, "message": "invalid request"}

    return generate_palette(query["prompt"][0])


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

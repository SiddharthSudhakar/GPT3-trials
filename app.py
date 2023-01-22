import os

import openai
from flask import Flask, redirect, render_template, request, url_for, session
#from blueprint import simple_page

app = Flask(__name__)
#app.register_blueprint(simple_page) #Added for blueprint

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/index-animal", methods=("GET", "POST"))
def index_animal():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-babbage-001",
            prompt=generate_prompt_animal(animal),
            temperature=0.6,
        )
        return redirect(url_for("index-animal", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index-animal.html", result=result)


def generate_prompt_animal(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )


# Chatbot route    
@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        start_sequence = "\nAI:"
        restart_sequence = "\nHuman: "
        chatbot = request.form["chatbot"]
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=generate_prompt_chatbot(chatbot),
            temperature=0,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
            )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt_chatbot(chatbot):
    return """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman:{}""".format(
        chatbot.capitalize()
    )
import os
import openai
import json
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("AI_API_KEY")
openai.api_key = API_KEY

class Generator:
    def __init__(self, temp, grade_level, min_sentences, max_sentences, model, max_tokens):
        self.temperature = temp
        self.grade_level = grade_level
        self.min_sentences = min_sentences
        self.max_sentences = max_sentences
        self.model = model
        self.max_tokens = max_tokens
    
    def create_prompt(self):
        return f"Summarize this in at least {self.min_sentences} sentences and at most {self.max_sentences} sentences for a {self.grade_level}-grade student:\n\nText: "
        
    def append_text(self, text):
        return text + "\n\nSummary: "

    def generate(self, text):
        prompt = self.create_prompt()
        prompt += self.append_text(text)
        completion = openai.Completion.create(  engine = self.model, 
                                                temperature = self.temperature, 
                                                prompt = prompt, 
                                                max_tokens = self.max_tokens,
                                                frequency_penalty = 1.0
                                                )
        completion_text = completion.choices[0].text
        return completion_text

class Summary:
    def __init__(self, title, body, url, generator, id):
        self.title = title
        self.body = body
        self.url = url
        self.generator = generator
        self.summarized_body = self.generator.generate(self.body)
    
    def print_summarized_text(self):
        print(self.summarized_body)

#text-davinci-002, temp = 0.8

summaries = []

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "dev",
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.post('/create_summary')
    def create_summary():
        data = request.json
        summaries.append(Summary(data["title"], data["body"], data["generator"], Generator(0.8, 12, 5, 10, "text-davinci-002", 300)))
    
    @app.post('/clear_summaries')
    def create_summary():
        summaries = []

    @app.get("/get_summaries")
    def get_summaries():
        return summaries

    @app.get("/total_summary")
    def total_summary():
        return summarize_summaries(summaries)

    return app

def summarize_summaries(summaries):
    bodies = [s.summarized_body for s in summaries]
    print(bodies)
    complete_body = "\n\n\n".join(bodies)
    return Summary("Compiled Summary", complete_body, "studytron9000.tech", Generator(0.8, 12, 10, 15, "text-davinci-002", 800))
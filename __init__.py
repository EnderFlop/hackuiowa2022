import os
import openai
import json
from flask_cors import cross_origin, CORS
from flask import Flask, request, jsonify, Response
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
    
    def create_summary_prompt(self, text):
        return f"Summarize this in at least {self.min_sentences} sentences and at most {self.max_sentences} sentences for a {self.grade_level}-grade student:\n\nText: {text}\n\nSummary: "

    def generate_summary(self, text):
        prompt = self.create_summary_prompt(text)
        completion = openai.Completion.create(  engine = self.model, 
                                                temperature = self.temperature, 
                                                prompt = prompt, 
                                                max_tokens = self.max_tokens,
                                                frequency_penalty = 1.0
                                                )
        completion_text = completion.choices[0].text
        return completion_text

    def generate_quiz(self, text):
        prompt = f"Make a three question, college-level, multiple choice quiz:\n\n{text}"
        completion = openai.Completion.create(  engine = self.model, 
                                                temperature = self.temperature, 
                                                prompt = prompt, 
                                                max_tokens = self.max_tokens,
                                                frequency_penalty = 1.0
                                                )
        completion_text = completion.choices[0].text
        return completion_text

    def generate_answer(self, text):
        prompt = f"Choose the correct answer:\n\n{text}"
        completion = openai.Completion.create(  engine = self.model, 
                                                temperature = self.temperature, 
                                                prompt = prompt, 
                                                max_tokens = self.max_tokens,
                                                frequency_penalty = 1.0
                                                )
        completion_text = completion.choices[0].text
        return completion_text

class Summary:
    def __init__(self, title, body, url, generator):
        self.title = title
        self.body = body
        self.url = url
        self.generator = generator
        self.summarized_body = self.generator.generate_summary(self.body)
        self.quiz = self.generator.generate_quiz(self.body)
        self.answers = None
    
    def print_summarized_text(self):
        print(self.summarized_body)
    
    def generate_answers(self):
        self.answers = self.generator.generate_answer(self.quiz)

#text-davinci-002, temp = 0.8

global summaries
summaries = []

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
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
        summaries.append(Summary(data["title"], data["body"], data["url"], Generator(0.8, 12, 5, 10, "text-davinci-002", 300)))
        return jsonify(success=True)
    
    @app.post('/clear_summaries')
    def clear_summary():
        summaries.clear()
        return jsonify(success=True)

    @app.get("/get_summaries")
    def get_summaries():
        if not summaries:
            return []
        all_summaries = [{"title": s.title, "summarized_body": s.summarized_body, "body": s.body, "url": s.url} for s in summaries]
        response = jsonify(all_summaries)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @app.get("/total_summary")
    def total_summary():
        if not summaries:
            return []
        s = summarize_summaries(summaries)
        response = jsonify({"title": s.title, "summarized_body": s.summarized_body, "body": s.body, "url": s.url})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @app.get('/generate_answers')
    def generate_quiz_answers():
        for s in summaries:
            s.generate_answers()
        return jsonify(success=True)

    @app.get('/quiz')
    def quiz():
        answers_to_quizes = [{s.quiz: s.answers} for s in summaries]
        response = jsonify(answers_to_quizes)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    return app

def summarize_summaries(summaries):
    bodies = [s.summarized_body for s in summaries]
    print(bodies)
    complete_body = "\n\n\n".join(bodies)
    return Summary("Compiled Summary", complete_body, "studytron9000.tech", Generator(0.8, 12, 10, 15, "text-davinci-002", 800))
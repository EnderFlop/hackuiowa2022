import os
import openai
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
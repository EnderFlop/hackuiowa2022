import os
import openai
from dotenv import load_dotenv
from summary import Summary
from generator import Generator

#text-davinci-002, temp = 0.8

def summarize_summaries(summaries):
    bodies = [s.summarized_body for s in summaries]
    print(bodies)
    complete_body = "\n\n\n".join(bodies)
    generator = Generator(0.8, 12, 10, 15, "text-davinci-002", 800)
    new_summary = Summary("Compiled Summary", complete_body, "studytron9000.tech", generator)
    print(new_summary.print_summarized_text())

if __name__ == "__main__":
    summaries = []
    generator = Generator(0.8, 12, 5, 10, "text-davinci-002", 300)
    for i in range(2):
        with open(f"./inputs/input{i}.txt", encoding="UTF-8") as text:
            summaries.append(Summary(f"Civil War {i}", text.read(), "history.com", generator))

    summarize_summaries(summaries)
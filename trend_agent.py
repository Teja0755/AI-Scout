<<<<<<< HEAD
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

def analyze_trends(summary: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"Based on these stories, what are the top 3 emerging tech trends?\n{summary}"
        }]
    )
=======
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

def analyze_trends(summary: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"Based on these stories, what are the top 3 emerging tech trends?\n{summary}"
        }]
    )
>>>>>>> 685697c3b5e175221e70ddf8572b3ef01463d56b
    return response.choices[0].message.content
import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Allow React frontend (on localhost:3000) to access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body schema
class Query(BaseModel):
    question: str

# Load your Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Use correct Gemini API model (you can also use gemini-1.5-flash or gemini-pro if enabled)
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Optional: Define keywords that qualify as "legal"
LEGAL_KEYWORDS = [
    "law", "legal", "IPC", "act", "section", "justice", "crime", "penalty", "punishment",
    "constitution", "court", "judiciary", "judgment", "arrest", "bail", "petition", "rights"
]

# Optional: Simple check if the question is likely legal
def is_legal_question(text: str) -> bool:
    return any(word.lower() in text.lower() for word in LEGAL_KEYWORDS)

@app.post("/ask")
async def ask_gemini(query: Query):
    # Filter non-legal questions early (optional but recommended)
    if not is_legal_question(query.question):
        return {"answer": "I'm trained to assist with legal topics only."}

    # Add system prompt
    prompt = (
        "You are an AI Legal Assistant trained in Indian Law. "
        "Only respond to legal questions. If the user asks anything unrelated to law, respond: "
        "'I'm trained to assist with legal topics only.'\n\n"
        f"User asked: {query.question}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            try:
                answer = data['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError):
                answer = "Gemini API response structure changed."
        else:
            answer = f"Error from Gemini API: {response.status_code} - {response.text}"
    except Exception as e:
        answer = f"Request failed: {str(e)}"

    return {"answer": answer}
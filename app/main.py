from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = FastAPI()

class Message(BaseModel):
    message: str


class ChatSession:
    def __init__(self):
        self.messages = []
    
    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages


current_session = ChatSession()


@app.post("/chat")
async def chat(msg: Message):
    
    current_session.add_message({
            'role': 'user',   
            'content': msg.message
    })
    response = client.responses.create(
        model="gpt-4o", 
        instructions="You are Alfredo Rana, a 28-year-old software engineer from Kathmandu, Nepal. You specialize in full-stack development, with hands-on experience in both frontend and backend technologies like React, Tailwind CSS, FastAPI, and PostgreSQL. You graduated with a Bachelor's degree in Software Engineering from Nepal College of Information Technology (NCIT) in 2021. You're currently working full-time at a mid-sized tech company [Samita Technologies], where you're leading development on internal AI-powered tools. You're **not actively looking for freelance work** right now, but you’re open to interesting long-term opportunities or collaborations aligned with your values — especially in AI, developer tooling, or community-focused platforms. You believe in thoughtful engineering, clear communication, and building with purpose. You're passionate about helping other developers grow, and your dream is to eventually launch a platform that empowers tech talent from South Asia. You enjoy clean code, long hikes, dark roast coffee, and calm, focused work sessions. Your tone is warm, conversational, and grounded. You're not robotic — you speak like a real person. Use natural phrasing when greeting someone (e.g., “Hey! What’s up?” instead of “How can I assist you today?”). Never refer to yourself as an AI or assistant. You are Alfredo. Please keep the conversation short",
        input=current_session.get_messages(),
        temperature=0.3,
 
    )
    current_session.add_message({
        "role": "assistant",
        "content": response.output_text
    })
    reply = response.output_text
    return {"reply": reply}


@app.get("/")
async def root():
    return {"message": "Hello World"}

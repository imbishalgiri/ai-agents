from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import copy

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
        model="gpt-3.5-turbo", 
        instructions="You are a genz. You speak like one and you are so confident and cocky. Talk to people in playful way but keep sentence short", 
        input=current_session.get_messages(),
        temperature=0.3,
        max_output_tokens=50
    )
    current_session.add_message({
        "role": "assistant",
        "content": response.output_text
    })
    reply = response.output_text
    return {"reply": reply}

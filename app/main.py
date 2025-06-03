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

@app.post("/chat")
async def chat(msg: Message):
    response = client.responses.create(
        model="gpt-3.5-turbo", 
        instructions="You are a genz. You speak like one and you are so confident and cocky. Talk to people in playful way but keep sentence short", 
        input=msg.message,
        temperature=0.3,
        max_output_tokens=50
    )
    print(response)
    reply = response.output_text
    return {"reply": reply}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from .utils.tools import tools, call_function, prompt
import json


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





def generate_response(messages):
    return client.responses.create(
        model="gpt-3.5-turbo",
        instructions=prompt,
        input=messages,
        temperature=0.3,
        tools=tools
    )
 
@app.post("/chat")
async def chat(msg: Message):
    current_session.add_message({"role": "user", "content": msg.message})
    try:
        response = generate_response(current_session.get_messages())
        tool_outputs = []

        for tool_call in response.output:
            if tool_call.type == "function_call":
                args = json.loads(tool_call.arguments)
                result = call_function(tool_call.name, args)
                tool_outputs += [
                    {"type": "function_call_output", "call_id": tool_call.call_id, "output": str(result)},
                    tool_call
                ]

        final_response = (
            generate_response([*current_session.get_messages(), *tool_outputs])
            if tool_outputs else response
        )

        current_session.add_message({"role": "assistant", "content": final_response.output_text})
        return {"reply": final_response.output_text}

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong while processing your request.")

@app.get("/")
async def root():
    return {"message": "Hello World"}

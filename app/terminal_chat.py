import requests
import json

FASTAPI_URL = "http://127.0.0.1:8000/chat"

def send_message(message: str) -> str | None:
    headers = {'Content-Type': 'application/json'}
    payload = {"message": message}
    
    try:
        response = requests.post(FASTAPI_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()   
        return response.json().get("reply")
    except requests.exceptions.ConnectionError:
        print("Err: Couldn't connect to the FastAPI server.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Err: {e}")
        return None

def chat_interface():
    print("--------------------------------------------------")
    print("Welcome to the Alfredo Chatbot! Type 'exit' to quit.")
    print("--------------------------------------------------")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("--------------------------------------------------")
            print("Bye, fam! Stay hydrated.")
            print("--------------------------------------------------")
            break
        
        reply = send_message(user_input)
        if reply:
            print(f"Alfredo: {reply}")
        
        print("---------------------------------------------------------") 

if __name__ == "__main__":
    chat_interface()
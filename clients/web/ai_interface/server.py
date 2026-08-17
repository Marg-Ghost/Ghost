from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import requests
import sys

CORE_URL = "http://0.0.0.0:4000/chat" 

app = FastAPI()

class payload(BaseModel):
    role: str = "user"
    content: str

@app.post("/")
async def chat(message: payload) -> str:
    try:
        response = requests.post(
            CORE_URL,
            json={"role": message.role, "content": message.content},
            timeout=60
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[Fehler] Konnte den Core nicht erreichen: {e}")
        return "[Error] Could not reach the core server"

    data = response.json()
    assistant_message = data["response"]
    return assistant_message


if __name__ == "__main__":
    uvicorn(app, host="0.0.0.0",port = 4100)
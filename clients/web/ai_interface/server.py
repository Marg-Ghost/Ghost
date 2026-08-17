from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import requests
import sys
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from fastapi.responses import FileResponse

CORE_URL = "http://0.0.0.0:4000/chat" 

app = FastAPI()

class payload(BaseModel):
    role: str = "user"
    content: str

app.mount("/static", StaticFiles(directory="web"), name="static")

@app.get("/")
async def load_surface():
	try:
		file_path = Path("/app/web/index.html")
		return FileResponse(str(file_path))
	except Exception as e:
		raise HTTPException(status_code=404, detail="index.html")

@app.post("/chat")
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
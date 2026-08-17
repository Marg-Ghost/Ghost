from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import requests
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

CORE_URL = "http://127.0.0.1:4000/chat"
BASE_DIR = Path(__file__).resolve().parent / "web"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class payload(BaseModel):
    role: str = "user"
    content: str

app.mount("/static", StaticFiles(directory=str(BASE_DIR)), name="static")

@app.get("/")
async def load_surface():
    index_file = BASE_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_file)

@app.post("/chat")
async def chat(message: payload) -> str:
    try:
        response = requests.post(
            CORE_URL,
            json={"role": message.role, "content": message.content},
            timeout=60,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[Fehler] Konnte den Core nicht erreichen: {e}")
        return "[Error] Could not reach the core server"

    data = response.json()
    assistant_message = data["response"]
    return assistant_message


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4100)

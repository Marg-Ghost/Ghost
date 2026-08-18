from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import uvicorn

import ollama_ai
import brain

app = FastAPI()


class ChatRequest(BaseModel):
    role: str = "user"
    content: str

class ManualEntryRequest(BaseModel):
    content: str


@app.post("/chat")
async def request_chat(user_request: ChatRequest, background_task : BackgroundTasks) -> dict:
    message = {"role": user_request.role, "content": user_request.content}
    print("server: ", message)
    answer = ollama_ai.chat(message, background_task)
    print("answer: ", answer)
    return {"response": answer}


@app.post("/manual-entry")
async def manual_entry(entry_request: ManualEntryRequest) -> dict:
    result = brain.summarize_for_storage(entry_request.content) 
    return {"entries": result}

import brain
import ollama_ai

@app.get("/memory/short")
async def get_short_memory() -> dict:
    return {"memory": ollama_ai.short_memory}

@app.get("/memory/long")
async def get_long_memory() -> dict:
    return {"memory": brain.documents}
    

if __name__ == "__main__" :
    uvicorn.run(app, host="0.0.0.0", port=4000)

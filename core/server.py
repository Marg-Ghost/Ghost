from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

import ollama_ai

app = FastAPI()


class ChatRequest(BaseModel):
    role: str = "user"
    content: str


@app.post("/chat")
async def request_chat(user_request: ChatRequest) -> dict:
    message = {"role": user_request.role, "content": user_request.content}
    answer = ollama_ai.chat(message)
    return {"response": answer}

    

if __name__ == "__main__" :
    uvicorn.run(app, host="0.0.0.0", port=4000)

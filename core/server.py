from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

import ollama_ai

app = FastAPI()


class ChatRequest(BaseModel):
    messages: list[dict]

@app.post("/chat")
async def request_chat (user_request : ChatRequest):
    input = user_request.messages
    response = ollama_ai.chat(input)

    return response
    

if __name__ == "__main__" :
    uvicorn.run(app, host="0.0.0.0", port=4000)
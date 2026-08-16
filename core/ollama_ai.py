import ollama
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
client = ollama.Client(host=OLLAMA_HOST)
current_model = "llama3.2:3b"

max_memory = 10
short_memory = []

def chat (input : dict) -> str:
    clear_m = handle_memory(input)
    if clear_m == 1:
       return {'response': 'the short term memory has been cleared'}
    response = client.chat(
                model = current_model,
                messages = short_memory,
                keep_alive = -1
            )
    
    content = response["message"]["content"]
    short_memory.append({"role": "assistant", "content": content})
    #a_message = {"role": "assistant", "content": response["message"]["content"]}
    
    return content

# First in First out
def handle_memory(input : str) -> int:
    global short_memory
    if input == "clear":
        short_memory = []
        return 1

    short_memory.append(input)
    if len(short_memory) > max_memory:
        short_memory.pop(0)
    return 0

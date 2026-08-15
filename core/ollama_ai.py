import ollama

client = ollama.Client(host='http://127.0.0.1:11434')
current_model = "llama3.2:3b"

short_memory = []

def chat (input : str) -> str:
    response = client.chat(
                model = current_model,
                messages = input,
                keep_alive = -1
            )
    
    return response
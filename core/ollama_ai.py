import ollama

client = ollama.Client(host='http://127.0.0.1:11434')
current_model = "llama3.2:3b"

max_memory = 10
short_memory = []

def chat (input : dict) -> str:
    handle_memory(input)
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
def handle_memory(input : str):
    short_memory.append(input)
    if len(short_memory) > max_memory:
        short_memory.pop(0)
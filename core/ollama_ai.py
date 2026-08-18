import ollama
import os

#my
import brain

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
client = ollama.Client(host=OLLAMA_HOST)
current_model = "qwen2.5:1.5b"

max_memory = 15
short_memory = []

def chat (input_message : dict, background_task = None) -> str:
    type_interaction = mode(input_message["content"])
    handle_memory(input_message, background_task)

    if type_interaction == 1:
       return {'response': 'the short term memory has been cleared'}

    brain_intel = ""
    if type_interaction == 0:
        brain_intel = brain.init_brain(input_message["content"])

    pass_message = [{"role": "system", "content":"Long Term Memory: "+ str(brain_intel)}] + short_memory
    response = client.chat(
                model = current_model,
                messages = pass_message,
                keep_alive = -1
            )
    
    content = response["message"]["content"]    
    return content

def mode(input_message : str) -> int:
    global short_memory
    if input_message == "clear":
            short_memory = []
            return 1
    if input_message == "simple":
            short_memory = []
            return 2 

    return 0

# First in First out
already_inside = 0
def handle_memory(input_message : dict, background_task = None):
    global short_memory
    global already_inside

    short_memory.append(input_message)

    if len(short_memory) > max_memory:
        if already_inside == 0:
            if background_task:
                background_task.add_task(brain.remember, short_memory.copy())
            else:
                brain.remember(short_memory)
            
            already_inside = max_memory 
        already_inside -= 1
        short_memory.pop(0)

import requests
import sys

CORE_URL = "http://0.0.0.0:4000/chat" 

def main() -> int:
    frame_h = "||"
    frame = frame_h +"=" * (25+18) + frame_h
    wellcome = frame_h + "Start Service 010 -> Ghost                 " + frame_h
    exit = frame_h + "Exit the Programm with 'exit'/'stop'/'kill'" + frame_h
    print(frame+"\n"+wellcome+"\n"+exit+"\n"+frame+"\n")

    message_number = 0
    while True:
        sign_pers = "|| User |:  "
        sign = "|| ^_^  |:  "
        frame_chat = "-" * 20
        
        print(frame_h, message_number, "|" ,frame_chat)
        message_number += 1
        message = input(sign_pers)

        if message == "exit" or message == "stop" or message == "kill":
            print(sign + "Goodbye!")
            break

        try:
            response = requests.post(
                CORE_URL,
                json={"role": "user", "content": message},
                timeout=60
            )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"[Fehler] Konnte den Core nicht erreichen: {e}")
            continue

        data = response.json()
        assistant_message = data["response"]

        print(f"{sign}{assistant_message}\n")
        #conversation_history.append({"role": "assistant", "content": assistant_message})
    
    return 0

if __name__ == "__main__":
    main()

        


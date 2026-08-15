import requests
import sys

CORE_URL = "http://0.0.0.0:4000/chat" 

def main() -> int:
    frame = "||"+"=" * 25
    wellcome = "||Start Service 001 -> Ghost"
    exit = "||Exit the Programm with 'exit'/'stop'/'kill'"
    print(frame+"\n"+wellcome+"\n"+exit+"\n"+frame+"\n")

    while True:
        sign_pers = "|| User |:  "
        sign = "|| ^_^ |:  "
        message = input (sign_pers)

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
        assistant_message = data["message"]["content"]   # Struktur kommt von Ollamas Response

        print(f"{sign}{assistant_message}\n")
        #conversation_history.append({"role": "assistant", "content": assistant_message})
    
    return 0

if __name__ == "__main__":
    main()

        


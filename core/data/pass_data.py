import json
import requests
import uuid

CORE_URL = "http://127.0.0.1:4000/manual-entry"
doc = []
ids = []

def main() -> int:
    global doc
    global ids
    frame_h = "||"
    frame = frame_h +"=" * (25+18) + frame_h
    wellcome = frame_h + "Start Service 001 -> DB entry              " + frame_h
    exit = frame_h + "Terminate the Programm with 'exit'/'stop'/'kill'" + frame_h
    print(frame+"\n"+wellcome+"\n"+exit+"\n"+frame+"\n")

    #mode = input(f"{frame_h} Mode? (s/l) : ")
    entry = input(f"{frame_h} Entry to DB |: ")

    terminate = ("exit", "stop", "kill")
    if entry in terminate:
        print(frame_h + "Goodbye! ")
        return 
    try:
        response = requests.post(
            CORE_URL, 
            json={"content": entry}, 
            timeout=60)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"[Fehler] Konnte den Core nicht erreichen: {e}")
        return

    data = response.json()
    print(f"{frame_h} Addition to DB | Erfolg : {len(data['entries'])} Einträge hinzugefügt")
    for e in data["entries"]:
        print(f"[Fehler] : {e}")

if __name__ == "__main__":
    main()
import json

def load_txt() -> tuple[list, list]:
    try:
        data = []
        with open(f"Vector_intel.txt", "r") as f:
            data = json.load(f)
        doc , ids = data
        return doc , ids
    except FileNotFoundError:
            return [], []

def save_txt(doc : list, ids : list):
    data = []
    data.append(doc)
    data.append(ids)
    with open(f"Vector_intel.txt", "w") as f:
        json.dump(data, f, indent=4)
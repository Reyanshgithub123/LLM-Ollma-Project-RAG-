import json

def load_text():

    with open("../structured_ocr.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = []

    for page in data["pages"]:
        for line in page["lines"]:
            texts.append(line["text"])

    return "\n".join(texts)

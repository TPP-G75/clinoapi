from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import spacy

class Note(BaseModel):
    text: str

app = FastAPI()
nlp = spacy.load("es_core_news_md")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/notes")
def analyze_note(note: Note):
    doc = nlp(note.text)
    entities = [
        {"text": ent.text, "start": ent.start_char, "end": ent.end_char, "label": ent.label_}
        for ent in doc.ents
    ]
    return {"Entities": entities}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)
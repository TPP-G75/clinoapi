from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import spacy
import ollama


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
        {
            "text": ent.text,
            "start": ent.start_char,
            "end": ent.end_char,
            "label": ent.label_,
        }
        for ent in doc.ents
    ]
    return {"Entities": entities}


@app.post("/llm")
def extract_terms(note: Note):
    prompt_template = f""" Eres un medico experto con capacidad de reconocer terminos medicos
    Extrae del siguiente texto, las palabras o oraciones cortas que representen terminos
    medicos que representen sintomas, malestares, condiciones medicas, tratamientos,
    etcetera, y los retornes como items de una lista de 10 items.

    No agregues una expliacion de los terminos extraidos y no incluyas otras palabras
    que no sean los terminos extraidos en la respuesta. La respuesta solo debe
    contener la lista  sin numerar Además, no incluyas palabras que sean sinónimos
    o representen la misma patología, y la respuesta debe  estar en español

    {note.text}"""

    response = ollama.generate(model="llama2", prompt=prompt_template)["response"]

    # TODO: send to the snostorm api the response of the model to get the snomed codes
    return {"response": response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

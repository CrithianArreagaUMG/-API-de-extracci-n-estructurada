import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
from fastapi import FastAPI
from pydantic import BaseModel
from models import ExtractResponse
import json
import openai

app = FastAPI()
class ExtractRequest(BaseModel):
    text: str
    domain: str

def build_prompt(text: str, domain: str) -> str:
    return f"""
Objetivo:
Analizar el texto proporcionado y devolver un JSON estructurado con información clave.

Reglas:
- No inventar información que no esté explícita en el texto.
- Respetar estrictamente el formato de salida definido.
- Si el texto es ambiguo o incompleto:
  - needs_clarification = true
  - Incluir al menos 2 preguntas en clarifying_questions.
- Si el texto es claro:
  - needs_clarification = false
  - clarifying_questions = [].

Formato de salida (OBLIGATORIO):
{{
  "summary": string (máx. 60 palabras),
  "entities": [
    {{ "name": string, "type": "PERSON" | "ORG" | "DATE" | "LOCATION" | "OTHER" }}
  ],
  "actions": [string],
  "confidence": number (entre 0 y 1),
  "needs_clarification": boolean,
  "clarifying_questions": [string]
}}

Texto a analizar:
"{text}"

Dominio:
"{domain}"

Instrucciones finales:
- Devuelve únicamente el JSON, sin explicaciones adicionales.
- Asegúrate de que el JSON sea válido y cumpla con el contrato.
"""

@app.post("/extract", response_model=ExtractResponse)
def extract_info(request: ExtractRequest):
    prompt = build_prompt(request.text, request.domain)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    parsed = json.loads(response["choices"][0]["message"]["content"])
    return ExtractResponse(**parsed)

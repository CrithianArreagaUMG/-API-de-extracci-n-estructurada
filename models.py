from pydantic import BaseModel #validar y documentar la entrada/salida de la API.
from typing import List, Literal #listas y valores literales (opciones fijas).

class Entity(BaseModel): # Hereda de BaseModel, así que FastAPI puede validar automáticamente su estructura.
    name: str
    type: Literal["PERSON", "ORG", "DATE", "LOCATION", "OTHER"]

class ExtractResponse(BaseModel): # Definimos la clase ExtractResponse, que es el contrato de salida de nuestro endpoint.
    summary: str
    entities: List[Entity]  # entities: una lista de objetos Entity (como el definido arriba).
    actions: List[str]  # actions: lista de acciones sugeridas en forma de strings.
    confidence: float  # confidence: número entre 0 y 1 que indica qué tan seguro está el sistema.
    needs_clarification: bool  # needs_clarification: booleano que indica si falta información (true/false).
    clarifying_questions: List[str]  # clarifying_questions: lista de preguntas para pedir aclaración.

from pydantic import BaseModel


class Card(BaseModel):
    id: str 
    question: str 
    solution: str 
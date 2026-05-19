from pydantic import BaseModel,EmailStr,Field
from datetime import datetime

class LeadCreate(BaseModel):
    """
    Donnees recues depuis le formulaire web.
    Fast API valide automatiquement chaque champ
    avant d'appeller la fonction de la route.

    """

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(min_length=1, max_length=100)
    phone: str | None = None
    message: str = ''
    source: str = "website"

class LeadResponse(BaseModel):
    """
    Donnees retournees apres la creation du lead.
    Fast API serialise automatiquement  cet object en JSON.
    """

    id: int
    name: str
    email: str
    created_at: datetime
    status: str  # "created" ou "duplicate"

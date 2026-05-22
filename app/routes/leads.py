from fastapi import APIRouter
from app.models.lead import LeadCreate
from app.services import lead_service

router = APIRouter()


@router.post("/leads",status_code=201)

async def create_lead(lead: LeadCreate):

    """
    recoit le JSON du formulaire.
    delegue entierement a lead_service.
    Ne contient aucune logiqu metier
    """

    return await lead_service.process_lead(lead)


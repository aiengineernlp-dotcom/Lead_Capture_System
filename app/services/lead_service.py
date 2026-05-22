# app/services/lead_service.py
import logging
from app.models.lead import LeadCreate
from app.db import repository
from app.services import email_service

logger = logging.getLogger(__name__)


async def process_lead(lead: LeadCreate)-> dict:

    """
    point d'entrer unique pour tout nouveau lead.
    Orchestre: deduplication -> sauvegarde -> emails.
    La route Fast API appelle uniquement cette fonction.
    """

    #Regle 1-  pour verifier si le lead existe deja
    existing = await repository.find_by_email(lead.email)
    if existing:
        return {
            "status": "duplicated",
            "id": existing["id"]
        }

    #Regle 2- sauvegarder en base de donnees dabords
    saved = await repository.save_lead(lead)

    #Regle 3 - pour  envoyer les email apres:
    await _send_emails(lead, saved["id"])
    return {
        "status": "created",
        "id": saved["id"]

    }

async def _send_emails(lead : LeadCreate, lead_id: int):
    """
    Fonction privee envoir les deux emails.
    si l'email echour , on loggue mais on ne propage pas .
    le lead est deja en BD il n'est pas perdu.
    """
    try:
        await  email_service.send_confirmation(
            to_email=lead.email,
            name = lead.name,
        )
        await email_service.send_agency_alert(
            lead = {"name": lead.name, "email": lead.email, "message": lead.message},
            lead_id = lead_id,

        )
    except Exception as e:
        logger.error(f"Email failed for lead {lead_id}: {e}")


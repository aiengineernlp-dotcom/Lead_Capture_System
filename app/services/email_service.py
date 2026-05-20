# app/services/email_service.py

import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)


async def send_confirmation(to_email: str, name: str) -> bool:
    """
    Email 1 : confirmation envoyée au lead.
    Rassure le lead et crée la première impression Tensoratech.
    """
    message = Mail(
        from_email=os.environ["FROM_EMAIL"],
        to_emails=to_email,
        subject="Votre demande est bien reçue — Tensoratech",
        html_content=f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px;">
            <h2>Bonjour {name},</h2>
            <p>
                Merci pour votre intérêt pour nos services
                d'automatisation IA et SEO.
            </p>
            <p>
                Notre équipe a bien reçu votre demande et vous
                contactera sous <strong>24h</strong>.
            </p>
            <p>
                En attendant, découvrez nos services sur
                <a href="https://tensoratech.com">tensoratech.com</a>.
            </p>
            <br>
            <p>— L'équipe Tensoratech</p>
        </div>
        """
    )
    return await _send(message)


async def send_agency_alert(lead, lead_id: int) -> bool:
    """
    Email 2 : alerte interne envoyée à Tensoratech.
    Contient toutes les infos du lead pour traitement rapide.
    """
    message = Mail(
        from_email=os.environ["FROM_EMAIL"],
        to_emails=os.environ["AGENCY_EMAIL"],
        subject=f"Nouveau lead #{lead_id} — {lead['name']}",
        html_content=f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px;">
            <h2>Nouveau lead entrant</h2>
            <table style="border-collapse: collapse; width: 100%;">
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;
                               font-weight: bold;">ID</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">
                        #{lead_id}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;
                               font-weight: bold;">Nom</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">
                        {lead['name']}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;
                               font-weight: bold;">Email</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">
                        {lead['email']}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;
                               font-weight: bold;">Message</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">
                        {lead['message']}</td>
                </tr>
            </table>
        </div>
        """
    )
    return await _send(message)


async def _send(message: Mail) -> bool:
    """
    Fonction privée — envoie le message via l'API SendGrid.
    Retourne True si envoyé, False si erreur.
    Ne propage jamais l'exception — le lead est déjà en DB.
    """
    try:
        sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
        response = sg.send(message)

        if response.status_code == 202:
            return True

        logger.warning(f"SendGrid status inattendu: {response.status_code}")
        return False

    except Exception as e:
        logger.error(f"SendGrid erreur: {e}")
        return False
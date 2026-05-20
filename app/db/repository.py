from app.db.database import database
from app.models.lead import LeadCreate

async def save_lead(lead: LeadCreate)-> dict:
    """
    Inserer un nouveau lead dans la base de donnees.
    Retourne l'id et le timestamp generer par PosgreSQL.
    """


    query = """
    INSERT INTO leads (name, email, phone, message,source)
    VALUES (:name, :email, :phone, :message, :source)
    RETURNING id, name, email, created_at 
    """

    result = await database.fetch_one(query=query, values = lead.model_dump(exclude={"status"} if hasattr(lead, "status") else set()))

    return dict(result)


async def find_by_email(email: str)-> dict | None:
    """
    cherche un lead dans la base de donnee par email.
    Retourne NONe si pas trouvee - Utiliser pour la deduplication
    """
    query = """
     SELECT id, email, created_at FROM leads WHERE email=:email
     LIMIT 1
     """
    result = await database.fetch_one(query=query, values={"email": email})

    return dict(result) if result else None



async def get_all_leads() -> list | None:
    """
    Retourne tous les leads present dnas la base de donnees du plus recent au plus ancien
    utiliser par le dashboard de l'entreprise Tensoratech.
    """

    query = """
    SELECT id, name, email, phone,message,source,created_at FROM leads
    ORDER BY created_at DESC 
    LIMIT 100 
    """
    result = await database.fetch_all(query=query)

    return [dict(r) for r in result]





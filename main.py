from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db.database import database
from app.routes.leads import router

app = FastAPI(title="Tensoratech Lead Capture")


# enregistre la route avec le prefice /api
app.include_router(router, prefix="/api")


# sert les fichiers HTML/ CSS/ JS du dossier frontend/

app.mount("/", StaticFiles(directory="frontend",html=True), name="frontend")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


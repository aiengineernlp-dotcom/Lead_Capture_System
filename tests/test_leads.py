# tests/test_leads.py

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from main import app


@pytest.mark.asyncio
async def test_create_lead_success():
    """
    Chemin heureux : lead valide → 201 + status created.
    On mocke la DB et SendGrid — pas de vrais appels externes.
    """
    with patch(
        'app.db.repository.save_lead',
        new_callable=AsyncMock,
        return_value={
            "id": 1,
            "name": "Ahmed",
            "email": "ahmed@tensoratech.com",
            "created_at": "2026-01-01T00:00:00"
        }
    ), patch(
        'app.db.repository.find_by_email',
        new_callable=AsyncMock,
        return_value=None          # pas de doublon
    ), patch(
        'app.services.email_service.send_confirmation',
        new_callable=AsyncMock,
        return_value=True
    ), patch(
        'app.services.email_service.send_agency_alert',
        new_callable=AsyncMock,
        return_value=True
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            res = await client.post("/api/leads", json={
                "name": "Ahmed Al Mansouri",
                "email": "ahmed@tensoratech.com",
                "message": "Test automatisé"
            })

        assert res.status_code == 201
        assert res.json()["status"] == "created"
        assert "id" in res.json()


@pytest.mark.asyncio
async def test_create_lead_invalid_email():
    """
    Email invalide → 422 automatique de Pydantic.
    Pas besoin de mocker — Pydantic bloque avant la DB.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        res = await client.post("/api/leads", json={
            "name": "Ahmed",
            "email": "pas-un-email"
        })

    assert res.status_code == 422


@pytest.mark.asyncio
async def test_create_lead_duplicate():
    """
    Email déjà en DB → 201 + status duplicated.
    find_by_email retourne un lead existant.
    """
    with patch(
        'app.db.repository.find_by_email',
        new_callable=AsyncMock,
        return_value={"id": 5, "email": "ahmed@tensoratech.com"}
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            res = await client.post("/api/leads", json={
                "name": "Ahmed",
                "email": "ahmed@tensoratech.com",
                "message": "Doublon"
            })

        assert res.status_code == 201
        assert res.json()["status"] == "duplicated"
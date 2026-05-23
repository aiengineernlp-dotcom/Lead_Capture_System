# Lead Capture System
### by [Tensoratech](https://tensoratech.com) — AI Automation + SEO for SMEs

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Tests](https://img.shields.io/badge/Tests-3%20passed-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## What it does

A production-ready lead capture system that automatically:

- Captures leads from a web form (name, email, phone, message)
- Validates every field before touching the database
- Detects duplicates — no double entries, no double emails
- Stores leads permanently in PostgreSQL
- Fires 2 automated emails via SendGrid:
  - **Confirmation** to the lead → professional first impression
  - **Alert** to the agency → instant notification with all lead details
- Protected by automated tests — nothing breaks silently

**No human intervention required. Works 24/7.**

---

## Built for

SMEs in Dubai and Abu Dhabi that want to:
- Capture consultation requests from their website
- Respond professionally and automatically
- Never lose a lead due to manual processes

---

## Architecture

```
Frontend (HTML/CSS/JS)
    ↓ POST /api/leads (JSON)
FastAPI Route
    ↓ Pydantic validation
Business Logic (lead_service.py)
    ├── Duplicate check → find_by_email()
    ├── Save to DB      → save_lead()
    └── Send emails     → email_service.py
            ├── Confirmation → Lead
            └── Alert        → Tensoratech
```

**Key principles applied:**
- Single responsibility — each file does one thing
- Repository pattern — SQL lives only in `repository.py`
- Least privilege — API keys scoped to minimum permissions
- Named SQL parameters — protected against SQL injection
- Async/await — non-blocking, handles concurrent requests

---

## Project structure

```
lead-capture/
├── main.py                        ← FastAPI entry point
├── requirements.txt
├── .env.example                   ← Required env variables
├── pytest.ini
├── PRODUCTION.md                  ← Pre-launch checklist
│
├── app/
│   ├── routes/leads.py            ← POST /api/leads
│   ├── models/lead.py             ← Pydantic models
│   ├── services/
│   │   ├── lead_service.py        ← Business logic
│   │   └── email_service.py       ← SendGrid
│   └── db/
│       ├── database.py            ← PostgreSQL connection
│       ├── repository.py          ← SQL queries
│       └── migrations/
│           ├── 001_create_leads.sql
│           └── 002_add_email_index.sql
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── form.js
│
├── tests/
│   └── test_leads.py              ← 3 automated tests
│
└── infra/
    └── docker-compose.yml         ← PostgreSQL local
```

---

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/tensoratech/lead-capture.git
cd lead-capture
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your values
```

Required variables:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
SENDGRID_API_KEY=SG.your_key_here
FROM_EMAIL=hello@yourdomain.com
AGENCY_EMAIL=team@yourdomain.com
```

### 3. Start PostgreSQL

```bash
docker-compose -f infra/docker-compose.yml up -d
```

### 4. Run migrations

```bash
psql -h localhost -U admin -d tensoratech_leads \
  -f app/db/migrations/001_create_leads.sql

psql -h localhost -U admin -d tensoratech_leads \
  -f app/db/migrations/002_add_email_index.sql
```

### 5. Launch

```bash
uvicorn main:app --reload
```

Open **http://localhost:8000** — the form is live.
Open **http://localhost:8000/docs** — API documentation.

---

## Run tests

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_leads.py::test_create_lead_success       PASSED
tests/test_leads.py::test_create_lead_invalid_email PASSED
tests/test_leads.py::test_create_lead_duplicate     PASSED

3 passed in 0.66s
```

Tests use mocks — no real DB or email calls during testing.

---

## API

### `POST /api/leads`

**Request body:**
```json
{
  "name": "Ahmed Al Mansouri",
  "email": "ahmed@company.com",
  "phone": "+971 50 123 4567",
  "message": "I need an SEO audit"
}
```

**Responses:**

| Status | Body | Meaning |
|--------|------|---------|
| `201` | `{"status": "created", "id": 42}` | Lead saved, emails sent |
| `201` | `{"status": "duplicated", "id": 17}` | Email already exists |
| `422` | Pydantic error detail | Invalid data |

---

## Tech stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | FastAPI (Python) | Fast, async, auto-docs |
| Validation | Pydantic v2 | Type-safe, EmailStr |
| Database | PostgreSQL 16 | Robust, production-grade |
| DB driver | asyncpg + databases | Non-blocking queries |
| Email | SendGrid | Reliable delivery |
| Container | Docker | Consistent environment |
| Tests | pytest + httpx | Async test support |

---

## Need this for your business?

Tensoratech builds custom automation systems for SMEs in Dubai and Abu Dhabi.

**Contact us:** [tensoratech.com](https://tensoratech.com)

---

*Built by Tensoratech — AI Automation + SEO for SMEs*
*Abu Dhabi, UAE*

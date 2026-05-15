# BSOP: Autonomous Hiring Intelligence Platform

BSOP is a production-grade AI recruiting intelligence system designed to stabilize LinkedIn extraction, automate profile intelligence, and provide a premium recruiter dashboard.

## Features
- **Stabilized LinkedIn Engine**: Card-first extraction with React hydration stabilization.
- **LLM Intent Parsing**: Automatically extracts roles, skills, and seniority from natural language queries.
- **Distributed Architecture**: FastAPI backend with Celery workers and Redis queue.
- **Intelligence Dashboard**: Next.js 14 frontend with Linear-style high-density UI.
- **Anti-Detection**: Built-in stealth hardening and humanized browser behavior.

## Quick Start

### 1. Environment Setup
Create a `.env` file in the root:
```env
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://bsop_user:bsop_password@localhost/bsop_intelligence
REDIS_URL=redis://localhost:6379/0
```

### 2. Start Services with Docker
```bash
docker-compose up --build
```

### 3. Backend (Local Development)
```bash
cd backend
pip install -r ../requirements.txt
uvicorn app.main:app --reload
```

### 4. Frontend (Local Development)
```bash
cd frontend
npm install
npm run dev
```

## Architecture
See `implementation_plan.md` and `frontend_architecture.md` for deep-dives into the system design.
```
core/             # Shared logic (Extraction, Intelligence, Adapters)
backend/          # FastAPI & Celery Worker
frontend/         # Next.js Application
debug/            # Extraction snapshots and HTML dumps
```

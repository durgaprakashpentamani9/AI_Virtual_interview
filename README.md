# InterviewIQ

LIVE URL: aivirtualinterview.vercel.app

AI assisted virtual interview practice with a React/Vite client and a Python FastAPI server.

## Features

- Register and sign in with a personal account.
- Upload and manage PDF, DOCX, or TXT resumes.
- Configure practice sessions by role, interview type, difficulty, and format.
- With a resume selected, alternate between resume based prompts and coding problems.
- Answer by typing or recording audio; browser speech synthesis can read questions aloud.
- Review answer feedback, speech metrics, interview reports, and score history.
- Camera preview stays in the browser; video frames are not uploaded.

## Requirements

- Python 3.11+
- Node.js 20+

## Run locally (PowerShell)

Open two terminals from the project root.

### Backend

```powershell
cd server
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
py -m uvicorn app.main:app --reload --port 8000
```

Replace `py -3.13` with your installed Python version if needed.

### Frontend

```powershell
cd client
npm install
Copy-Item .env.example .env
npm run dev
```

Open <http://localhost:5173>. API documentation: <http://localhost:8000/docs>.

## Demo account

- Email: `demo@interviewiq.ai`
- Password: `Password@123`

Sample data is seeded at server startup when `SEED_SAMPLE_DATA=true`.

## Configuration

Copy `server/.env.example` to `server/.env`. The defaults use a local SQLite database and local resume storage. Set a strong `JWT_SECRET` before deployment.

| Server variable | Purpose |
| --- | --- |
| `PORT` | API port (default: `8000`) |
| `CLIENT_URL` | Allowed client origin (default: `http://localhost:5173`) |
| `DATABASE_URL` | SQLAlchemy database URL; SQLite is the local default |
| `JWT_SECRET` | Secret used to sign authentication tokens |
| `JWT_EXPIRES_MINUTES` | Token lifetime |
| `GEMINI_API_KEY`, `GEMINI_MODEL` | Optional Gemini configuration |
| `GROQ_API_KEY`, `GROQ_STT_MODEL` | Optional cloud speech transcription |
| `EMBEDDING_MODEL` | Embedding model setting |
| `TTS_PROVIDER`, `ELEVENLABS_API_KEY` | Speech output settings |
| `STORAGE_PROVIDER` | Resume storage mode (local by default) |
| `SUPABASE_URL`, `SUPABASE_KEY` | Optional Supabase settings |
| `MAX_AUDIO_MB` | Audio upload size limit |
| `SEED_SAMPLE_DATA` | Seed demo user and sample history |

Gemini and Groq keys are optional for local startup. Without them, questions use the local question bank and voice transcription is unavailable. Keep secrets on the server and out of Git.

Copy `client/.env.example` to `client/.env`:

```dotenv
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_BASE_URL=ws://localhost:8000/ws
```

Only public service URLs belong in client environment variables.

## Project structure

```text
client/                 React, Vite, and Tailwind application
  src/api/               Axios API client
  src/hooks/             Media, speech, and WebSocket hooks
  src/store/             Zustand state
  src/main.jsx           Pages and routes
server/                  FastAPI application
  app/core/               Configuration
  app/data/               Roles, skills, and starter questions
  app/db/                 Database session and demo seeding
  app/models/             SQLAlchemy models
  app/repositories/       Data access layer
  app/services/           Cloud AI service integration
  app/main.py             API and WebSocket routes
  alembic/                Database migration setup
  tests/                  API flow tests
```

## Database and deployment

SQLite is intended for local development. For deployment, set `DATABASE_URL` to a PostgreSQL connection string and `CLIENT_URL` to the deployed frontend origin. Configure HTTPS/WSS at your hosting provider. Keep API keys on the server.

## Run the API flow test

From the `server` directory with dependencies installed:

```powershell
py -m pytest tests -q -p no:cacheprovider
```

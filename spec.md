====================================================================
PROJECT NAME
====================================================================
 
InterviewIQ - AI Virtual Interview System (Online / Internet-Based)
 
====================================================================
PROJECT TYPE
====================================================================
 
React + Python (FastAPI) + Cloud AI APIs, real-time online virtual
interview web application with speech, video, and resume intelligence
 
====================================================================
PRIMARY OBJECTIVE
====================================================================
 
Build an ONLINE AI Virtual Interview web application where a user can:
 
1. register / login from any device using the internet
2. upload a resume (PDF / DOCX / TXT)
3. choose job role, interview type, and difficulty
4. join a live virtual interview room with an AI interviewer
5. hear each question in AI voice
6. answer by speaking (webcam + microphone) or by typing
7. get speech-to-text transcript of the answer
8. get answer score + feedback after every answer
9. get speech analysis (speaking speed, filler words, pauses)
10. get video analysis (face visible, eye contact, head position)
11. get a final interview report with strengths, weaknesses, and tips
12. view interview history, score trends, and execution trace
 
IMPORTANT:
This is NOT a generic chatbot.
This is NOT an offline / local app. It REQUIRES an internet connection.
 
This IS:
- an online real-time virtual interview system with an AI interviewer
- resume parsing + skill extraction + skill-based question generation
- cloud speech-to-text + text-to-speech interview conversation
- a 6-stage agentic pipeline powered by cloud LLM APIs
- answer evaluation with score + feedback
- speech and body-language feedback
- final report generation
- deployed on the internet with a public URL (HTTPS)
 
====================================================================
IMPORTANT PROJECT STRUCTURE
====================================================================
 
THE PROJECT ROOT CONTAINS:
 
- client/   (React frontend)
- server/   (Python FastAPI backend)
 
DO NOT CREATE:
- frontend/
- backend/
 
USE client/ AND server/ ONLY.
 
====================================================================
CORE CONSTRAINTS
====================================================================
 
- Frontend inside client/ only (JavaScript + React)
- Backend inside server/ only (Python)
- Internet connection is REQUIRED (online application)
- Agentic AI workflow architecture
- real-time interview using WebSocket (WSS in production)
- cloud AI through API calls (free tiers preferred)
- all API keys stay on the server in .env, NEVER in client code
- cloud database (hosted PostgreSQL)
- HTTPS required in production (needed for camera + microphone access)
- must not use fake placeholder implementations
- AI provider code must be behind a service layer so a provider can be
  swapped without changing agents
 
====================================================================
ONLINE AI SERVICES (FREE TIER FIRST)
====================================================================
 
LLM (questions, feedback, report)
- Google Gemini API (model: gemini-2.0-flash) - free tier available
- Optional alternative: Groq API (llama-3.1-70b-versatile) via same service
  interface
 
SPEECH TO TEXT
- Groq API, Whisper model (whisper-large-v3-turbo) - free tier available
- Optional alternative: Deepgram API
 
TEXT TO SPEECH (AI interviewer voice)
- Browser speechSynthesis (default, free, no key)
- Optional upgrade: ElevenLabs API or Google Cloud Text-to-Speech
 
EMBEDDINGS (semantic similarity, answer vs ideal answer)
- Gemini embedding API (text-embedding-004)
 
VIDEO ANALYSIS
- MediaPipe Tasks Vision (Face Landmarker) running inside the browser
  (loaded from CDN over internet). Only numeric metrics are sent to server.
  No video is uploaded.
 
====================================================================
FINAL TECH STACK
====================================================================
 
FRONTEND (client/)
------------------
- React 18
- Vite
- TailwindCSS
- React Router
- TanStack React Query
- Zustand
- react-hook-form
- axios
- native WebSocket API (real-time interview channel)
- MediaDevices API + MediaRecorder API (webcam + microphone)
- Web Speech API (speechSynthesis for AI voice)
- @mediapipe/tasks-vision (face and eye-contact metrics in browser)
- react-webcam (webcam preview)
- recharts (score charts)
- lucide-react (icons)
 
BACKEND (server/)
-----------------
- Python 3.11+
- FastAPI
- Uvicorn + Gunicorn (production ASGI)
- WebSockets (FastAPI native)
- Pydantic v2 (validation)
- SQLAlchemy 2.x (ORM)
- PostgreSQL (hosted cloud DB, via DATABASE_URL)
- Alembic (database migrations)
- python-jose (JWT)
- passlib[bcrypt] (password hashing)
- python-multipart (file upload)
- pdfplumber (PDF text extraction)
- python-docx (DOCX text extraction)
- spaCy (resume entity + skill extraction)
- scikit-learn (TF-IDF and cosine similarity helpers)
- google-generativeai (Gemini SDK)
- httpx (async calls to Groq / Deepgram / other APIs)
- tenacity (retry with backoff for API calls)
- slowapi (rate limiting)
- python-dotenv
- pytest (testing)
 
CLOUD / DEPLOYMENT
------------------
- Frontend hosting: Vercel or Netlify
- Backend hosting: Render or Railway
- Database hosting: Neon or Supabase (PostgreSQL)
- Resume file storage: Supabase Storage or Cloudinary
  (or server disk for development)
- Source control + CI: GitHub (GitHub Actions optional)
- HTTPS + WSS enabled by hosting platform
 
====================================================================
RUNNING PORTS / RUNTIME DEFAULTS (LOCAL DEVELOPMENT)
====================================================================
 
Frontend (Vite): localhost:5173
Backend (FastAPI): localhost:8000
PostgreSQL (local dev, optional): localhost:5432
 
API base in client: VITE_API_BASE_URL or http://localhost:8000/api
WebSocket base in client: VITE_WS_BASE_URL or ws://localhost:8000/ws
 
PRODUCTION
Frontend: https://<your-app>.vercel.app
Backend:  https://<your-api>.onrender.com
WebSocket: wss://<your-api>.onrender.com/ws
 
====================================================================
FINAL PROJECT STRUCTURE
====================================================================
 
interviewiq/
|
+-- client/
|   +-- src/
|       +-- api/
|       +-- components/
|       +-- pages/
|       +-- store/
|       +-- hooks/       (useWebcam, useRecorder, useSpeechSynthesis,
|       |                 useInterviewSocket, useFaceMetrics)
|       +-- utils/
|       +-- main.jsx
|       +-- router.jsx
|       +-- index.css
|
+-- server/
|   +-- app/
|   |   +-- core/         (config, security, logging)
|   |   +-- db/           (session, base, init, seed)
|   |   +-- models/       (SQLAlchemy models)
|   |   +-- schemas/      (Pydantic schemas)
|   |   +-- repositories/ (data access layer)
|   |   +-- services/     (llm_service, stt_service, tts_service,
|   |   |                  embedding_service, resume_service,
|   |   |                  scoring_service, storage_service)
|   |   +-- agents/       (planner, resume_analyzer, question_generator,
|   |   |                  answer_evaluator, speech_analyzer, report_writer)
|   |   +-- api/          (routers: auth, resumes, interviews, reports,
|   |   |                  dashboard, meta)
|   |   +-- ws/           (interview websocket handler)
|   |   +-- middleware/
|   |   +-- utils/
|   |   +-- data/         (question_bank.json, skills.json, roles.json,
|   |   |                  filler_words.json)
|   |   +-- main.py
|   +-- scripts/
|   +-- uploads/          (dev only)
|   +-- logs/
|   +-- requirements.txt
|   +-- tests/
|
+-- .env
+-- README.md
 
====================================================================
MANDATORY IMPLEMENTATION RULES
====================================================================
 
CLIENT FOLDER
-------------
The ENTIRE frontend MUST be implemented ONLY inside /client.
This includes pages, routes, interview room, webcam and recorder hooks,
face metrics hook, WebSocket hook, Zustand store, Tailwind setup, axios
API calls, forms, auth UI, dashboard, report pages, and charts.
 
SERVER FOLDER
-------------
The ENTIRE backend MUST be implemented ONLY inside /server.
This includes FastAPI app, REST APIs, WebSocket handler, agents, pipeline,
resume parsing, cloud AI service calls, scoring, database models, auth,
file uploads, error handling, and logging.
 
STRICT RULES
------------
1. NEVER create additional frontend/backend root folders.
2. ALWAYS use /client and /server.
3. ALL frontend code MUST remain inside /client.
4. ALL backend code MUST remain inside /server.
5. SQLAlchemy models MUST exist inside /server/app/models.
6. All data access MUST go through the repository layer.
7. All cloud AI calls MUST go through /server/app/services only.
 
====================================================================
HOW THE SYSTEM WORKS
====================================================================
 
USER FLOW
---------
1. User opens the website and registers / logs in
2. User uploads a resume
3. System extracts text, skills, projects, education, experience
4. User creates an interview: role + type + difficulty + question count
5. User opens the interview room and allows camera + microphone
6. AI interviewer speaks the first question (text-to-speech)
7. User answers by voice (or text)
8. Audio is sent to server -> cloud speech-to-text -> transcript
9. Answer is evaluated by cloud LLM; speech metrics are calculated;
   video metrics come from the browser
10. Instant feedback is shown, then next question (or follow-up) is asked
11. After the last question, final report is generated
12. User reviews report, charts, history, and trace
 
AI FLOW
-------
Resume Upload
      |
Text Extraction (pdfplumber / python-docx / read)
      |
Resume Profile (spaCy + skills.json matching + Gemini cleanup)
      |
Create Interview Session (role, type, difficulty, count)
      |
Planner -> Resume Analyzer -> Question Generator   (Gemini API)
      |
AI speaks question (TTS) -> User answers (audio / text)
      |
Speech-to-Text (Groq Whisper API)
      |
Answer Evaluator (Gemini API) + Speech Analyzer (+ Video Metrics)
      |
Follow-up or Next Question  (repeat until done)
      |
Report Writer (Gemini API)
      |
InterviewReport saved (scores + strengths + weaknesses + tips + trace)
 
====================================================================
INTERVIEW OPTIONS
====================================================================
 
INTERVIEW TYPES
---------------
- technical
- hr
- behavioral
- resume_based
- mixed
 
DIFFICULTY LEVELS
-----------------
- easy (fresher)
- medium
- hard
 
JOB ROLES (starter list, stored in server/app/data/roles.json)
--------------------------------------------------------------
- Frontend Developer
- Backend Developer
- Full Stack Developer
- Python Developer
- Data Analyst
- AI / ML Engineer
- Software Engineer (general)
- Custom role (user types any role)
 
NUMBER OF QUESTIONS
-------------------
- 5, 8, or 10 (default 5)
 
INTERVIEW MODES
---------------
- voice + video mode (full experience)
- voice only mode (microphone only)
- text mode (no microphone, no camera)
 
====================================================================
DATA MODELS (SQL TABLES)
====================================================================
 
users: id, name, email (unique), password_hash, target_role, created_at
 
resumes: id, user_id, original_name, stored_name, file_url, mime_type, size,
         file_type, status, extracted_text, profile (JSON),
         processing_error, created_at
  file_type: pdf | docx | txt
  status: uploaded | processing | ready | failed
  profile: { skills[], projects[], education[], experience[], summary }
 
interview_sessions: id, user_id, resume_id (nullable), role, type,
                    difficulty, mode, total_questions, current_index,
                    status, plan (JSON), started_at, completed_at,
                    trace (JSON list)
  status: created | in_progress | completed | abandoned | failed
 
interview_questions: id, session_id, order_index, text, category,
                     difficulty, expected_keywords (JSON), ideal_answer,
                     is_follow_up, parent_question_id, source
  source: ai | bank
 
interview_answers: id, session_id, question_id, transcript, input_mode,
                   duration_sec, content_scores (JSON), speech_metrics (JSON),
                   video_metrics (JSON), feedback (JSON), created_at
  input_mode: voice | text
  content_scores: { relevance, clarity, depth, communication, overall }
                  (each 0-10)
  speech_metrics: { words_per_minute, filler_count, filler_words[],
                    pause_count, longest_pause_sec }
  video_metrics: { face_visible_pct, eye_contact_pct, head_steady_pct }
 
interview_reports: id, session_id (unique), overall_score, category_scores
                   (JSON), speech_summary (JSON), video_summary (JSON),
                   strengths (JSON), weaknesses (JSON), suggestions (JSON),
                   summary, verdict, trace (JSON), created_at
  verdict: needs_improvement | average | good | excellent
 
IMPORTANT:
- Raw audio and video are NOT stored. Audio is sent to the speech API for
  transcription and then deleted.
- Only transcript text and numeric metrics are saved.
 
====================================================================
STORAGE ARCHITECTURE
====================================================================
 
Use ONE repository layer for all data access.
 
- Database: hosted PostgreSQL (Neon / Supabase) through DATABASE_URL
- Connection pooling enabled (pool_pre_ping=True)
- Migrations managed with Alembic
- Resume files: cloud storage (Supabase Storage / Cloudinary) in production,
  local /server/uploads in development
 
Repository operations (generic):
get_all(model, filters, order_by)
get_by_id(model, id)
get_one(model, filters)
create(model, data)
update_by_id(model, id, updates)
upsert(model, filters, create_data, update_data)
delete_by_id(model, id)
delete_where(model, filters)
count(model, filters)
 
All routers/services MUST use this repository layer. Routers stay thin.
 
====================================================================
RESUME PARSING + QUESTION SOURCING
====================================================================
 
RESUME PARSING
--------------
- extract text: pdfplumber (PDF), python-docx (DOCX), direct read (TXT)
- clean text (remove extra spaces, broken lines, bullets)
- detect sections: skills, projects, education, experience
- skills matched against server/app/data/skills.json + spaCy entity hints
- Gemini API builds a clean profile JSON from the resume text
 
QUESTION SOURCING
-----------------
- Gemini generates questions from role + type + difficulty + resume profile
- each question comes with expected_keywords and an ideal_answer
- resume_based type: questions built from user's skills and projects
  (example: "Explain your project X. Which technology did you use and why?")
- question_bank.json is used only as a backup when an API call fails
  after retries
- never repeat a question inside one session
 
====================================================================
SPEECH PIPELINE
====================================================================
 
CAPTURE (client)
----------------
- MediaRecorder records microphone audio (webm/opus)
- one audio blob per answer
- send blob to server through WebSocket or
  POST /api/interviews/{id}/answer-audio
 
TRANSCRIBE (server)
-------------------
- send audio to Groq Whisper API through stt_service
- return transcript text
- user can edit transcript before final submit
- if transcription fails after retries: ask user to retry or switch to
  text answer
 
SPEECH ANALYSIS (server)
------------------------
- words_per_minute = word count / answer duration
  (ideal range 110-160 WPM)
- filler words counted from filler_words.json (um, uh, like, basically,
  you know, actually ...)
- pauses detected from word/segment timestamps returned by Whisper
- output is added to speech_metrics
 
AI VOICE (client)
-----------------
- speechSynthesis reads each question aloud
- mute / unmute toggle
- replay question button
 
====================================================================
VIDEO ANALYSIS
====================================================================
 
- runs INSIDE THE BROWSER with MediaPipe Face Landmarker
- every 500 ms while the user answers, the client calculates:
    face_visible_pct  - face detected in frame
    eye_contact_pct   - eyes looking toward camera (iris position estimate)
    head_steady_pct   - head position stays stable
- only these numbers are sent to the server (with the answer)
- video frames are NEVER uploaded or saved
- user can switch video analysis OFF in the setup page
- if camera is denied: interview continues in voice only or text mode
- video metrics are only for soft feedback, they must not change the
  content score
 
====================================================================
AI AGENT SYSTEM (6 STAGES)
====================================================================
 
PLANNER            - decide interview plan: topic order, category mix,
                     difficulty curve, number of questions
RESUME ANALYZER    - read resume profile, pick key skills and projects
                     to ask about
QUESTION GENERATOR - generate the next question or a follow-up question,
                     with expected keywords and ideal answer
ANSWER EVALUATOR   - score the transcript (0-10), write feedback, decide if
                     a follow-up is needed
SPEECH ANALYZER    - calculate speaking speed, filler words, pauses
                     (+ attach video metrics from client)
REPORT WRITER      - build final report: overall score, strengths,
                     weaknesses, suggestions, verdict
 
LLM RULES
---------
- all LLM calls go through llm_service (one place to change provider)
- ask the LLM for JSON output only, validate with Pydantic
- if JSON is invalid: retry once with a repair prompt
- set timeouts (15 seconds) and retries (3 attempts, exponential backoff)
 
====================================================================
WORKFLOW ENGINE
====================================================================
 
SESSION START PIPELINE
----------------------
Create session -> Planner -> Resume Analyzer -> Question Generator ->
save first question -> status in_progress
 
ANSWER PIPELINE (runs on every answer)
--------------------------------------
Receive audio/text -> Speech-to-Text -> Answer Evaluator + Speech Analyzer ->
save scores, metrics, feedback -> decide: follow-up | next question | finish ->
Question Generator (if more questions) -> send result through WebSocket ->
save trace
 
FINISH PIPELINE
---------------
All questions answered (or user ends early) -> Report Writer ->
save InterviewReport -> session status completed
 
Each session stores trace[] with: stage name, status, start time,
end time, provider used, and short note.
ALL stages MUST be trackable.
 
====================================================================
ANSWER EVALUATION RULES
====================================================================
 
SCORE PARTS (each 0-10)
-----------------------
- relevance: does the answer match the question?
  (LLM judgment + embedding similarity with ideal answer)
- clarity: is it clear and well structured?
- depth: does it show real knowledge and examples?
- communication: is the language simple and confident?
  (uses speech metrics: filler words, speed)
- overall: weighted average
  (relevance 35%, depth 30%, clarity 20%, communication 15%)
 
FEEDBACK OUTPUT (JSON)
----------------------
{
  "scores": { "relevance": 0, "clarity": 0, "depth": 0,
              "communication": 0, "overall": 0 },
  "feedback": "short feedback in simple English",
  "strengths": ["..."],
  "improvements": ["..."],
  "ideal_answer_hint": "short model answer",
  "needs_follow_up": false
}
 
====================================================================
API FAILURE HANDLING (ONLINE SERVICES)
====================================================================
 
The app is online, but cloud APIs can fail or hit free-tier limits.
Handle it safely:
 
- retry failed API calls 3 times with exponential backoff (tenacity)
- if the LLM still fails: use a question from question_bank.json and
  rule-based scoring (keyword coverage + answer length + filler words)
  for that one step, and mark the trace note as "backup"
- if speech-to-text fails: show "Could not hear you, try again" and allow
  switching to text answer
- if rate limit (HTTP 429) is hit: show a friendly "please wait" message
  and retry after the delay
- if the internet connection drops on the client: show an offline banner,
  pause the timer, and auto-reconnect the WebSocket when internet returns
- never crash the whole interview because one API call failed
 
====================================================================
API ENDPOINTS
====================================================================
 
HEALTH
GET /api/health
 
AUTH
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
 
RESUMES
GET    /api/resumes
POST   /api/resumes/upload
GET    /api/resumes/{id}
POST   /api/resumes/{id}/reprocess
DELETE /api/resumes/{id}
 
INTERVIEW SESSIONS
GET    /api/interviews
POST   /api/interviews                      (create + start session)
GET    /api/interviews/{id}
GET    /api/interviews/{id}/questions
POST   /api/interviews/{id}/answer          (text answer)
POST   /api/interviews/{id}/answer-audio    (audio answer, returns transcript
                                             + feedback + next question)
POST   /api/interviews/{id}/finish          (end early / generate report)
DELETE /api/interviews/{id}
 
REPORTS
GET /api/interviews/{id}/report
GET /api/reports
 
META
GET /api/meta/roles
GET /api/meta/question-types
GET /api/meta/system-status     (LLM, speech API, database availability)
 
DASHBOARD
GET /api/dashboard
 
WEBSOCKET
WS /ws/interviews/{id}?token=...
  client -> server events: audio_chunk, audio_end, video_metrics,
                           text_answer, end_interview
  server -> client events: question, transcript_partial, transcript_final,
                           feedback, speech_metrics, next_question,
                           report_ready, error
 
====================================================================
INTERVIEW PIPELINE GRAPH
====================================================================
 
Show 6 stages: Planner, Resume Analyzer, Question Generator,
Answer Evaluator, Speech Analyzer, Report Writer.
 
Activation rules:
- Planner active if an interview session exists
- Resume Analyzer active if the session has a ready resume
- Question Generator active if the session has at least one question
- Answer Evaluator active if at least one answer is evaluated
- Speech Analyzer active if at least one answer has speech metrics
- Report Writer active if a report exists for the session
 
Do NOT light up all nodes for a brand new session.
 
====================================================================
FRONTEND PAGES
====================================================================
 
PUBLIC
/login
/register
 
PROTECTED
/                                   (dashboard)
/resumes                            (upload + manage resumes)
/interviews                         (interview history list)
/interviews/new                     (setup: role, type, difficulty, count,
                                     resume, mode, device check)
/interviews/:sessionId              (INTERVIEW ROOM - most important page)
/interviews/:sessionId/report       (final report page)
 
INTERVIEW ROOM MUST CONTAIN
- AI interviewer panel (avatar + animated speaking indicator)
- webcam preview panel (user video, local only)
- progress bar (question 3 of 5)
- current question card (category + difficulty tag)
- replay question button + mute voice toggle
- mic button (start / stop recording) with live recording indicator
- transcript box (editable before submit)
- text answer box (for text mode)
- timer per question
- submit answer button + skip button
- instant feedback card after each answer (scores + speech metrics + tips)
- internet connection status indicator
- pipeline graph / trace panel (collapsible)
- end interview button (with confirm)
 
SETUP PAGE MUST CONTAIN
- role, type, difficulty, question count selectors
- resume selector
- mode selector (voice + video, voice only, text)
- device check (camera preview, mic level meter, speaker test)
- video analysis ON/OFF toggle
 
REPORT PAGE MUST CONTAIN
- overall score and verdict
- category score chart (recharts radar or bar)
- speech summary (average WPM, filler words, pauses)
- video summary (eye contact, face visible, head steady) if available
- question-by-question list (question, transcript, score, feedback,
  ideal answer hint)
- strengths, weaknesses, suggestions
- trace section
- button to retake the same interview
 
DASHBOARD MUST CONTAIN
- total interviews, average score, best score
- score trend line chart (last 10 interviews)
- recent interviews list
- quick start interview button
 
====================================================================
API CLIENT + STATE
====================================================================
 
- one axios instance: base URL from env, bearer token injection, logout on 401
- Zustand auth store: token, user; actions setSession, logout (persisted)
- Zustand interview store: current session, current question, timer,
  recording state, voice settings, device settings, online status
- hooks: useInterviewSocket (WebSocket connect, auto-reconnect, events),
  useRecorder (MediaRecorder), useWebcam (camera), useFaceMetrics
  (MediaPipe), useSpeechSynthesis (AI voice)
- React Query shared keys: auth user, dashboard, resumes, interviews,
  interview details, interview questions, report, system status
- invalidate queries after upload / create / answer / finish / delete
 
====================================================================
SECURITY REQUIREMENTS
====================================================================
 
- JWT auth (python-jose), bearer token verification
- WebSocket auth using token in query parameter
- passlib bcrypt password hashing
- email unique, password min length 6, invalid login returns 401
- HTTPS and WSS only in production
- all API keys (Gemini, Groq, etc.) only in server .env, never sent to client
- file validation: resume (PDF / DOCX / TXT, 5MB limit),
  audio (webm / wav / ogg, 10MB limit)
- every resource user-scoped, no cross-user data leakage
- CORS allowed only for CLIENT_URL
- rate limiting on auth and AI endpoints (slowapi)
- sanitize user answers before sending to the LLM prompt
  (limit length, strip prompt-injection style text)
- raw audio / video never stored
- errors returned as { "message": "..." }
 
====================================================================
ERROR HANDLING RULES
====================================================================
 
- global exception handlers in FastAPI
- httpError helper (raise HTTPException with status + message)
- handle: invalid login, invalid token, unsupported file type, upload too
  large, missing resume/session/report, unauthorized access, failed resume
  processing, empty answer, silent audio, transcription failure,
  answering a completed session, LLM timeout, API rate limit,
  WebSocket disconnect, client internet loss
- if WebSocket disconnects, client auto-reconnects and resumes the session
- if one stage fails, retry, then use backup and continue
 
====================================================================
SEED / DEMO MODE
====================================================================
 
Demo user:
email: demo@interviewiq.ai
password: Password@123
 
Provide a demo resume profile, 2 completed demo interviews (with reports),
and the starter question bank.
- seed demo data on first start if SEED_SAMPLE_DATA=true
 
====================================================================
ENV CONFIG
====================================================================
 
SERVER (.env)
PORT
CLIENT_URL
DATABASE_URL
JWT_SECRET
JWT_EXPIRES_MINUTES
GEMINI_API_KEY
GEMINI_MODEL
GROQ_API_KEY
GROQ_STT_MODEL
EMBEDDING_MODEL
TTS_PROVIDER
ELEVENLABS_API_KEY            (optional)
STORAGE_PROVIDER              (local | supabase | cloudinary)
SUPABASE_URL                  (optional)
SUPABASE_KEY                  (optional)
MAX_AUDIO_MB
SEED_SAMPLE_DATA
 
CLIENT (.env)
VITE_API_BASE_URL
VITE_WS_BASE_URL
 
If a required key is missing, the server must start and show a clear
message in /api/meta/system-status instead of crashing.
 
====================================================================
DEPLOYMENT
====================================================================
 
1. Push code to GitHub
2. Database: create hosted PostgreSQL on Neon / Supabase, copy DATABASE_URL
3. Backend: deploy server/ on Render / Railway
   - start command: gunicorn -k uvicorn.workers.UvicornWorker app.main:app
   - add all server env variables
   - run Alembic migrations on deploy
4. Frontend: deploy client/ on Vercel / Netlify
   - add VITE_API_BASE_URL and VITE_WS_BASE_URL (https / wss URLs)
5. Set CLIENT_URL on the backend to the deployed frontend URL (CORS)
6. Test camera + microphone on the HTTPS URL
7. Add a health check on /api/health
 
====================================================================
IMPLEMENTATION RULES FOR CODEX
====================================================================
 
1. Frontend: JavaScript + React ONLY. DO NOT use TypeScript.
2. Backend: Python + FastAPI ONLY. DO NOT use Node.js / Express.
3. USE SQLAlchemy with hosted PostgreSQL (SQLite allowed only for quick
   local testing).
4. NEVER create NestJS structure or Prisma schema.
5. USE modular FastAPI architecture (routers, services, agents,
   repositories).
6. ALL frontend code MUST remain inside /client.
7. ALL backend code MUST remain inside /server.
8. ALL data access MUST go through the repository layer.
9. ALL cloud AI calls MUST go through the services layer.
10. NEVER expose API keys in client code or Git history (.env in .gitignore).
11. Keep agent outputs structured to the defined JSON shapes.
12. Validate every LLM JSON response with Pydantic.
13. Keep routers thin; logic lives in services and agents.
14. Every protected resource MUST be user-scoped.
15. Resume upload MUST automatically trigger parsing.
16. ALL agent outputs MUST be JSON serializable.
17. ALL interview sessions MUST be trackable (status + trace).
18. A question must never repeat inside one session.
19. Raw audio and video MUST NEVER be stored.
20. Use async calls (httpx) for all cloud APIs so the event loop is not
    blocked.
21. Add retries, timeouts, and rate-limit handling to every cloud API call.
 
====================================================================
SUCCESS CRITERIA / ACCEPTANCE
====================================================================
 
PROJECT IS SUCCESSFUL IF:
- app is deployed and opens from a public HTTPS URL on the internet
- user can register, login, stay authenticated
- user can upload, reprocess, and delete resumes
- resume text and skills are extracted correctly
- user can create an interview with role, type, difficulty, count, mode
- device check works (camera, microphone, speaker)
- AI interviewer speaks every question aloud
- questions are generated online by the LLM, one by one, with no repeats
- user can answer by voice and the transcript appears (cloud STT)
- user can answer by text when voice is off or denied
- every answer gets scores, feedback, and an ideal answer hint
- speech metrics (WPM, filler words, pauses) are shown per answer
- video metrics (eye contact, face visible) work when camera is on
- follow-up questions appear when the answer is weak or unclear
- final report is generated with overall score, strengths, weaknesses, tips
- report page shows chart, question-by-question review, and trace
- dashboard shows counts, average score, and score trend
- pipeline graph reflects the real session state
- interview history can be viewed and deleted
- raw audio / video is never saved
- API keys are never visible in the browser
- interview does not crash when one cloud API call fails or is rate limited
- client shows a banner and auto-reconnects when internet drops
 
====================================================================
FINAL END-TO-END FLOW
====================================================================
 
Open website (internet) -> Register / Login
      |
Upload Resume
      |
Resume Parsing (extract -> clean -> profile via Gemini -> ready)
      |
Create Interview (role + type + difficulty + count + mode)
      |
Device Check -> Join Interview Room (WSS connected)
      |
Planner -> Resume Analyzer -> Question Generator   (cloud LLM)
      |
AI speaks question -> User answers (voice / text)
      |
Cloud Speech-to-Text -> Answer Evaluator + Speech Analyzer
(+ Video Metrics from browser)
      |
Feedback -> follow-up or next question
      |
Report Writer (cloud LLM)
      |
InterviewReport saved in cloud database
      |
View on dashboard, history, report page, pipeline graph
 
====================================================================
END OF FINAL IMPLEMENTATION SPEC
====================================================================
 
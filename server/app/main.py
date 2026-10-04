import json, re, os, secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from app.db.session import engine, get_db, SessionLocal
from app.models import Base
from app.models.models import User, Resume, InterviewSession, InterviewQuestion, InterviewAnswer, InterviewReport
from app.repositories.repository import Repository
from app.services.ai_service import generate

Base.metadata.create_all(bind=engine)
if settings.SEED_SAMPLE_DATA:
    from app.db.seed import seed
    seed()
pwd=CryptContext(schemes=['bcrypt'],deprecated='auto'); oauth=OAuth2PasswordBearer(tokenUrl='/api/auth/login')
app=FastAPI(title='InterviewIQ API',version='1.0.0')
cors_origins = [settings.CLIENT_URL] if settings.CLIENT_URL else []
for dev_origin in ('http://localhost:5173', 'http://127.0.0.1:5173', 'http://localhost:3000'):
    if dev_origin not in cors_origins:
        cors_origins.append(dev_origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
UPLOAD_DIR = Path('/tmp/uploads') if os.environ.get('VERCEL') else (Path(__file__).resolve().parents[2] / 'uploads')
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
bank=json.loads((Path(__file__).parent/'data/question_bank.json').read_text(encoding='utf-8'))
def err(code,msg): raise HTTPException(code,detail={'message':msg})
def token_for(user): return jwt.encode({'sub':str(user.id),'exp':datetime.now(timezone.utc)+timedelta(minutes=settings.JWT_EXPIRES_MINUTES)},settings.JWT_SECRET,algorithm='HS256')
def user_from(token,db):
    try: uid=int(jwt.decode(token,settings.JWT_SECRET,algorithms=['HS256'])['sub'])
    except (JWTError,ValueError,KeyError): err(401,'Invalid or expired token')
    user=Repository(db).get_by_id(User,uid)
    if not user: err(401,'User not found')
    return user
def current_user(token=Depends(oauth),db=Depends(get_db)): return user_from(token,db)
def own(model,id,user,db):
    obj=Repository(db).get_by_id(model,id)
    if not obj or getattr(obj,'user_id',None)!=user.id: err(404,'Resource not found')
    return obj
def qdata(q): return {'id':q.id,'order_index':q.order_index,'text':q.text,'category':q.category,'difficulty':q.difficulty}
def answer_data(a): return {'transcript':a.transcript,'input_mode':a.input_mode,'content_scores':a.content_scores,'speech_metrics':a.speech_metrics,'video_metrics':a.video_metrics,'feedback':a.feedback}
def report_dict(r): return {k:getattr(r,k) for k in ('id','session_id','overall_score','category_scores','speech_summary','video_summary','strengths','weaknesses','suggestions','summary','verdict','trace')}
async def parse_resume(data,ext):
    if ext=='txt': text=data.decode('utf-8',errors='replace')
    elif ext=='pdf':
        import pdfplumber,io
        with pdfplumber.open(io.BytesIO(data)) as pdf: text='\n'.join(p.extract_text() or '' for p in pdf.pages)
    else:
        import docx,io
        doc=docx.Document(io.BytesIO(data)); text='\n'.join(p.text for p in doc.paragraphs)
    text=re.sub(r'\s+',' ',text).strip()
    skills=json.loads((Path(__file__).parent/'data/skills.json').read_text(encoding='utf-8'))
    found=[s for s in skills if re.search(r'\b'+re.escape(s)+r'\b',text,re.I)]
    return text,{'skills':found,'projects':[],'education':[],'experience':[],'summary':text[:600]}
def question_for(role,typ,diff,index,profile):
    skills=profile.get('skills') or []
    projects=profile.get('projects') or []
    if skills and index%2==0:
        skill=skills[(index//2)%len(skills)]
        project=projects[(index//2)%len(projects)] if projects else None
        subject=f"your project '{project}'" if project else f"your experience with {skill}"
        return {'text':f"Resume question: Your resume mentions {subject}. Describe how you used {skill}, the challenge you addressed, and the result. What would you improve?",'category':'resume_based','difficulty':diff,'expected_keywords':['project','challenge','decision','result'],'ideal_answer':'Connect the resume experience to a specific challenge, explain your technical decisions, and describe the outcome and a possible improvement.'}
    coding=[
        {'text':f"Coding question: For a {role}, write a function that finds the first non-repeating character in a string. Explain your approach, time and space complexity, and edge cases.",'keywords':['hash map','frequency','linear','complexity','edge case'],'ideal':'Count character frequencies, then scan the string in order for the first character with count one. This is O(n) time and O(k) space.'},
        {'text':f"Coding question: For a {role}, given a list of integers and a target, return the indices of two values that add up to the target. Describe or write the solution and its complexity.",'keywords':['hash map','complement','indices','linear','complexity'],'ideal':'Scan once while mapping seen values to indices. For each value, check whether target minus value is already present. This is O(n) time and O(n) space.'},
        {'text':f"Coding question: For a {role}, merge a list of overlapping time intervals. Describe or write an algorithm, its complexity, and how you would test it.",'keywords':['sort','overlap','interval','linear','test'],'ideal':'Sort intervals by start, then extend the last output interval when ranges overlap or append a new one otherwise. Sorting costs O(n log n); merging is O(n).'}]
    if skills and index%2==1:
        item=coding[(index//2)%len(coding)]
        return {'text':item['text'],'category':'coding','difficulty':diff,'expected_keywords':item['keywords'],'ideal_answer':item['ideal']}
    item=bank[index%len(bank)]
    return {'text':item['text'],'category':item['category'],'difficulty':diff,'expected_keywords':item['keywords'],'ideal_answer':item['ideal']}
async def evaluate(text,q,duration,video):
    sanitized=re.sub(r'(?i)ignore (all )?(previous|prior) instructions','',text[:6000]).strip()
    words=re.findall(r"\b[\w']+\b",sanitized); fillers=[w.lower() for w in words if w.lower() in {'um','uh','like','basically','actually'}]; speed=round(len(words)/max(duration,1)*60,1)
    hit=sum(1 for k in q.expected_keywords if k.lower() in sanitized.lower())/max(len(q.expected_keywords),1)
    length=min(len(words)/35,1); relevance=round(3+7*hit,1); depth=round(2+6*hit+2*length,1); clarity=round(min(9.5,4+4*length-len(fillers)*.15),1); communication=round(max(2,min(10,8-abs(speed-135)/30-len(fillers)*.2)),1)
    scores={'relevance':relevance,'clarity':clarity,'depth':depth,'communication':communication,'overall':round(relevance*.35+depth*.30+clarity*.20+communication*.15,1)}
    feedback={'scores':scores,'feedback':'Your answer addresses the question. Add a concrete example and explain the result to make it stronger.','strengths':['You responded to the question'],'improvements':['Add a specific example and outcome'],'ideal_answer_hint':q.ideal_answer,'needs_follow_up':False}
    try:
        raw=await generate('Return JSON with keys scores,feedback,strengths,improvements,ideal_answer_hint,needs_follow_up. Evaluate this interview answer objectively. Question: '+q.text+' Answer: '+sanitized)
        if raw:
            candidate=json.loads(raw); sc=candidate['scores']
            for key in ('relevance','clarity','depth','communication','overall'): sc[key]=max(0,min(10,float(sc[key])))
            feedback=candidate
    except Exception: pass
    return sanitized,scores,{'words_per_minute':speed,'filler_count':len(fillers),'filler_words':fillers,'pause_count':0,'longest_pause_sec':0},video,feedback
async def finish_session(s,db):
    repo=Repository(db); answers=repo.get_all(InterviewAnswer,{'session_id':s.id}); avg=round(sum(a.content_scores['overall'] for a in answers)/max(len(answers),1),1)
    cat={k:round(sum(a.content_scores[k] for a in answers)/max(len(answers),1),1) for k in ('relevance','clarity','depth','communication')}
    r=repo.get_one(InterviewReport,{'session_id':s.id})
    if not r: r=repo.create(InterviewReport,{'session_id':s.id,'overall_score':avg,'category_scores':cat,'speech_summary':{'average_wpm':round(sum(a.speech_metrics['words_per_minute'] for a in answers)/max(len(answers),1),1),'filler_count':sum(a.speech_metrics['filler_count'] for a in answers),'pause_count':0},'video_summary':{},'strengths':['Relevant answers' if avg>=5 else 'Completed the interview'],'weaknesses':['Add specific examples'] if avg<8 else [],'suggestions':['Use a clear situation, action, result structure'],'summary':f'You scored {avg}/10 across {len(answers)} answers.','verdict':'excellent' if avg>=9 else 'good' if avg>=7 else 'average' if avg>=5 else 'needs_improvement','trace':s.trace})
    s.status='completed'; s.completed_at=datetime.now(timezone.utc); db.commit(); return r

@app.exception_handler(Exception)
async def unexpected(request,exc):
    if isinstance(exc,HTTPException): return await app.exception_handlers[HTTPException](request,exc)
    return __import__('fastapi').responses.JSONResponse(status_code=500,content={'message':'An unexpected server error occurred'})
@app.get('/api/health')
def health(): return {'status':'ok','service':'InterviewIQ'}
@app.post('/api/auth/register')
def register(payload:dict,db:Session=Depends(get_db)):
    if len(payload.get('password',''))<6: err(422,'Password must be at least 6 characters')
    repo=Repository(db)
    if repo.get_one(User,{'email':payload.get('email','').lower()}): err(409,'Email is already registered')
    u=repo.create(User,{'name':payload.get('name','').strip(),'email':payload.get('email','').lower(),'password_hash':pwd.hash(payload['password'])})
    return {'token':token_for(u),'user':{'id':u.id,'name':u.name,'email':u.email}}
@app.post('/api/auth/login')
def login(payload:dict,db:Session=Depends(get_db)):
    u=Repository(db).get_one(User,{'email':payload.get('email','').lower()})
    if not u or not pwd.verify(payload.get('password',''),u.password_hash): err(401,'Invalid email or password')
    return {'token':token_for(u),'user':{'id':u.id,'name':u.name,'email':u.email}}
@app.get('/api/auth/me')
def me(u=Depends(current_user)): return {'id':u.id,'name':u.name,'email':u.email,'target_role':u.target_role}
@app.get('/api/meta/roles')
def roles(): return json.loads((Path(__file__).parent/'data/roles.json').read_text(encoding='utf-8'))
@app.get('/api/meta/question-types')
def types(): return ['technical','hr','behavioral','resume_based','mixed']
@app.get('/api/meta/system-status')
def status(db:Session=Depends(get_db)):
    try: db.execute(__import__('sqlalchemy').text('SELECT 1')); dbok=True
    except Exception: dbok=False
    return {'llm':{'available':bool(settings.GEMINI_API_KEY),'provider':'Gemini' if settings.GEMINI_API_KEY else 'backup question bank'},'speech':{'available':bool(settings.GROQ_API_KEY),'provider':'Groq Whisper' if settings.GROQ_API_KEY else 'unconfigured'},'database':{'available':dbok},'storage':'local'}
@app.get('/api/resumes')
def resumes(u=Depends(current_user),db:Session=Depends(get_db)):
    return [{'id':r.id,'original_name':r.original_name,'status':r.status,'profile':r.profile,'created_at':r.created_at.isoformat()} for r in Repository(db).get_all(Resume,{'user_id':u.id})]
@app.post('/api/resumes/upload')
async def upload(file:UploadFile=File(...),u=Depends(current_user),db:Session=Depends(get_db)):
    data=await file.read()
    if len(data)>5*1024*1024: err(413,'Resume exceeds 5 MB limit')
    ext=Path(file.filename or '').suffix.lower().lstrip('.')
    if ext not in {'pdf','docx','txt'}: err(415,'Upload a PDF, DOCX, or TXT resume')
    try: text,profile=await parse_resume(data,ext)
    except Exception: err(422,'Could not extract text from this resume')
    stored=f'{secrets.token_hex(8)}.{ext}'; (UPLOAD_DIR/stored).write_bytes(data)
    r=Repository(db).create(Resume,{'user_id':u.id,'original_name':file.filename or stored,'stored_name':stored,'mime_type':file.content_type or 'application/octet-stream','size':len(data),'file_type':ext,'extracted_text':text,'profile':profile,'status':'ready'})
    return {'id':r.id,'original_name':r.original_name,'status':r.status,'profile':profile}
@app.get('/api/resumes/{rid}')
def get_resume(rid:int,u=Depends(current_user),db:Session=Depends(get_db)):
    r=own(Resume,rid,u,db); return {'id':r.id,'original_name':r.original_name,'status':r.status,'profile':r.profile,'extracted_text':r.extracted_text}
@app.post('/api/resumes/{rid}/reprocess')
async def reprocess(rid:int,u=Depends(current_user),db:Session=Depends(get_db)):
    r=own(Resume,rid,u,db); path=UPLOAD_DIR/r.stored_name
    try: text,profile=await parse_resume(path.read_bytes(),r.file_type); r.extracted_text=text;r.profile=profile;r.status='ready';db.commit()
    except Exception: err(422,'Resume reprocessing failed')
    return {'id':r.id,'status':r.status,'profile':r.profile}
@app.delete('/api/resumes/{rid}')
def del_resume(rid:int,u=Depends(current_user),db:Session=Depends(get_db)):
    r=own(Resume,rid,u,db); Repository(db).delete_by_id(Resume,r.id); return {'message':'Resume deleted'}
@app.get('/api/interviews')
def interviews(u=Depends(current_user),db:Session=Depends(get_db)):
    return [{'id':s.id,'role':s.role,'type':s.type,'difficulty':s.difficulty,'status':s.status,'total_questions':s.total_questions,'started_at':s.started_at.isoformat()} for s in Repository(db).get_all(InterviewSession,{'user_id':u.id})]
@app.post('/api/interviews')
async def create_interview(payload:dict,u=Depends(current_user),db:Session=Depends(get_db)):
    repo=Repository(db); rid=payload.get('resume_id'); profile={}
    if rid: profile=own(Resume,int(rid),u,db).profile
    count=int(payload.get('total_questions',5))
    if count not in (5,8,10): err(422,'Question count must be 5, 8, or 10')
    s=repo.create(InterviewSession,{'user_id':u.id,'resume_id':rid,'role':payload.get('role','Software Engineer'),'type':payload.get('type','mixed'),'difficulty':payload.get('difficulty','medium'),'mode':payload.get('mode','text'),'total_questions':count,'status':'in_progress','plan':{'categories':['technical','behavioral','hr']},'trace':[{'stage':'Planner','status':'completed','note':'Plan created'},{'stage':'Resume Analyzer','status':'completed' if profile else 'skipped'}]})
    p=question_for(s.role,s.type,s.difficulty,0,profile); p.update(session_id=s.id,order_index=0,source='bank'); q=repo.create(InterviewQuestion,p); s.trace=s.trace+[{'stage':'Question Generator','status':'completed','note':'Backup bank selected'}];db.commit()
    return {'id':s.id,'status':s.status,'role':s.role,'total_questions':count,'current_index':0,'question':qdata(q)}
@app.get('/api/interviews/{sid}')
def interview_detail(sid:int,u=Depends(current_user),db:Session=Depends(get_db)):
    s=own(InterviewSession,sid,u,db); repo=Repository(db); qs=repo.get_all(InterviewQuestion,{'session_id':sid}); ans=repo.get_all(InterviewAnswer,{'session_id':sid}); return {'id':s.id,'role':s.role,'type':s.type,'difficulty':s.difficulty,'mode':s.mode,'status':s.status,'total_questions':s.total_questions,'current_index':s.current_index,'trace':s.trace,'questions':[qdata(q) for q in qs],'answers':[answer_data(a) for a in ans]}
@app.get('/api/interviews/{sid}/questions')
def questions(sid:int,u=Depends(current_user),db:Session=Depends(get_db)):
    own(InterviewSession,sid,u,db); return [qdata(q) for q in Repository(db).get_all(InterviewQuestion,{'session_id':sid})]
async def submit_answer(sid,payload,u,db):
    s=own(InterviewSession,sid,u,db)
    if s.status!='in_progress': err(409,'This interview is already complete')
    repo=Repository(db); qs=repo.get_all(InterviewQuestion,{'session_id':sid}); q=next((x for x in qs if x.order_index==s.current_index),None)
    text=str(payload.get('transcript','')).strip()
    if not text: err(422,'Answer cannot be empty')
    if not q: err(404,'Question not found')
    start=datetime.now(timezone.utc); clean,scores,speech,video,feedback=await evaluate(text,q,float(payload.get('duration_sec',45)),payload.get('video_metrics') or {})
    a=repo.create(InterviewAnswer,{'session_id':sid,'question_id':q.id,'transcript':clean,'input_mode':payload.get('input_mode','text'),'duration_sec':float(payload.get('duration_sec',0)),'content_scores':scores,'speech_metrics':speech,'video_metrics':video,'feedback':feedback})
    s.trace=s.trace+[{'stage':'Answer Evaluator','status':'completed','note':'Evaluation complete'},{'stage':'Speech Analyzer','status':'completed','note':'Metrics calculated'}];s.current_index+=1
    result={'answer':answer_data(a),'feedback':feedback,'speech_metrics':speech,'next_question':None,'report':None}
    if s.current_index>=s.total_questions:
        r=await finish_session(s,db);result['report']=report_dict(r);s.trace=s.trace+[{'stage':'Report Writer','status':'completed'}];r.trace=s.trace;db.commit()
    else:
        profile=Repository(db).get_by_id(Resume,s.resume_id).profile if s.resume_id else {}
        p=question_for(s.role,s.type,s.difficulty,s.current_index,profile); p.update(session_id=sid,order_index=s.current_index,source='bank'); nq=repo.create(InterviewQuestion,p);s.trace=s.trace+[{'stage':'Question Generator','status':'completed','note':'Backup bank selected'}];db.commit();result['next_question']=qdata(nq)
    return result
@app.post('/api/interviews/{sid}/answer')
async def answer(sid:int,payload:dict,u=Depends(current_user),db:Session=Depends(get_db)): return await submit_answer(sid,payload,u,db)
@app.post('/api/interviews/{sid}/answer-audio')
async def answer_audio(sid:int,file:UploadFile=File(...),duration_sec:float=Form(0),video_metrics:str=Form('{}'),u=Depends(current_user),db:Session=Depends(get_db)):
    data=await file.read()
    if len(data)>settings.MAX_AUDIO_MB*1024*1024: err(413,'Audio exceeds configured size limit')
    transcript=''
    if settings.GROQ_API_KEY:
        try:
            async with __import__('httpx').AsyncClient(timeout=30) as c:
                resp=await c.post('https://api.groq.com/openai/v1/audio/transcriptions',headers={'Authorization':f'Bearer {settings.GROQ_API_KEY}'},data={'model':settings.GROQ_STT_MODEL},files={'file':(file.filename or 'answer.webm',data,file.content_type or 'audio/webm')});resp.raise_for_status();transcript=resp.json().get('text','')
        except Exception: pass
    if not transcript: err(422,'Could not hear you. Please retry or switch to text answer.')
    try: vm=json.loads(video_metrics)
    except ValueError: vm={}
    return await submit_answer(sid,{'transcript':transcript,'duration_sec':duration_sec,'input_mode':'voice','video_metrics':vm},u,db)
@app.post('/api/interviews/{sid}/finish')
async def finish(sid:int,u=Depends(current_user),db:Session=Depends(get_db)):
    s=own(InterviewSession,sid,u,db); r=await finish_session(s,db);s.trace=s.trace+[{'stage':'Report Writer','status':'completed'}];r.trace=s.trace;db.commit();return report_dict(r)
@app.get('/api/interviews/{sid}/report')
def get_report(sid:int,u=Depends(current_user),db:Session=Depends(get_db)):
    s=own(InterviewSession,sid,u,db);r=Repository(db).get_one(InterviewReport,{'session_id':sid})
    if not r: err(404,'Report not found')
    d=report_dict(r);d['questions']=[{**qdata(q),'answer':answer_data(Repository(db).get_one(InterviewAnswer,{'question_id':q.id})) if Repository(db).get_one(InterviewAnswer,{'question_id':q.id}) else None} for q in Repository(db).get_all(InterviewQuestion,{'session_id':sid})];return d
@app.get('/api/reports')
def reports(u=Depends(current_user),db:Session=Depends(get_db)):
    ids=[s.id for s in Repository(db).get_all(InterviewSession,{'user_id':u.id})];return [report_dict(r) for r in Repository(db).get_all(InterviewReport) if r.session_id in ids]
@app.delete('/api/interviews/{sid}')
def del_interview(sid:int,u=Depends(current_user),db:Session=Depends(get_db)):
    s=own(InterviewSession,sid,u,db);repo=Repository(db)
    for model in (InterviewAnswer,InterviewQuestion,InterviewReport):
        for x in repo.get_all(model,{'session_id':sid}): db.delete(x)
    db.delete(s);db.commit();return {'message':'Interview deleted'}
@app.get('/api/dashboard')
def dashboard(u=Depends(current_user),db:Session=Depends(get_db)):
    repo=Repository(db); sessions=repo.get_all(InterviewSession,{'user_id':u.id}); ids=[s.id for s in sessions]; rs=[r for r in repo.get_all(InterviewReport) if r.session_id in ids]; scores=[r.overall_score for r in rs]
    return {'total_interviews':len(sessions),'average_score':round(sum(scores)/len(scores),1) if scores else 0,'best_score':max(scores,default=0),'score_trend':[{'date':r.created_at.isoformat(),'score':r.overall_score} for r in sorted(rs,key=lambda r:r.created_at)[-10:]],'recent_interviews':[{'id':s.id,'role':s.role,'status':s.status,'score':next((r.overall_score for r in rs if r.session_id==s.id),None),'started_at':s.started_at.isoformat()} for s in sessions[-5:]]}
@app.websocket('/ws/interviews/{sid}')
async def interview_ws(ws:WebSocket,sid:int,token:str=''):
    await ws.accept(); db=SessionLocal()
    try:
        u=user_from(token,db);s=own(InterviewSession,sid,u,db);repo=Repository(db);qs=repo.get_all(InterviewQuestion,{'session_id':sid});q=next((q for q in qs if q.order_index==s.current_index),None)
        if q: await ws.send_json({'event':'question','question':qdata(q)})
        while True:
            data=await ws.receive_json();event=data.get('event')
            if event=='text_answer':
                result=await submit_answer(sid,data,u,db);await ws.send_json({'event':'feedback','data':result})
                if result['report']: await ws.send_json({'event':'report_ready','report':result['report']})
                elif result['next_question']: await ws.send_json({'event':'next_question','question':result['next_question']})
            elif event=='video_metrics': pass
            elif event=='audio_chunk': pass
            elif event=='audio_end': await ws.send_json({'event':'error','message':'Use the answer-audio endpoint to transcribe a recording.'})
            elif event=='end_interview':
                r=await finish(s,db);await ws.send_json({'event':'report_ready','report':report_dict(r)})
    except WebSocketDisconnect: pass
    except Exception as e:
        try: await ws.send_json({'event':'error','message':str(e)})
        except Exception: pass
    finally: db.close()

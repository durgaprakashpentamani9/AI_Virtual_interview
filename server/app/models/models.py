from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Text, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.models import Base

def now(): return datetime.now(timezone.utc)
class User(Base):
    __tablename__='users'
    id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(100)); email: Mapped[str]=mapped_column(String(255),unique=True,index=True); password_hash: Mapped[str]=mapped_column(String(255)); target_role: Mapped[str|None]=mapped_column(String(120),nullable=True); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class Resume(Base):
    __tablename__='resumes'
    id: Mapped[int]=mapped_column(primary_key=True); user_id: Mapped[int]=mapped_column(ForeignKey('users.id')); original_name: Mapped[str]=mapped_column(String(255)); stored_name: Mapped[str]=mapped_column(String(255)); mime_type: Mapped[str]=mapped_column(String(120)); size: Mapped[int]=mapped_column(Integer); file_type: Mapped[str]=mapped_column(String(10)); status: Mapped[str]=mapped_column(String(20),default='ready'); extracted_text: Mapped[str]=mapped_column(Text,default=''); profile: Mapped[dict]=mapped_column(JSON,default=dict); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class InterviewSession(Base):
    __tablename__='interview_sessions'
    id: Mapped[int]=mapped_column(primary_key=True); user_id: Mapped[int]=mapped_column(ForeignKey('users.id')); resume_id: Mapped[int|None]=mapped_column(ForeignKey('resumes.id'),nullable=True); role: Mapped[str]=mapped_column(String(120)); type: Mapped[str]=mapped_column(String(30)); difficulty: Mapped[str]=mapped_column(String(20)); mode: Mapped[str]=mapped_column(String(20)); total_questions: Mapped[int]=mapped_column(Integer); current_index: Mapped[int]=mapped_column(Integer,default=0); status: Mapped[str]=mapped_column(String(20),default='created'); plan: Mapped[dict]=mapped_column(JSON,default=dict); trace: Mapped[list]=mapped_column(JSON,default=list); started_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); completed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
class InterviewQuestion(Base):
    __tablename__='interview_questions'
    id: Mapped[int]=mapped_column(primary_key=True); session_id: Mapped[int]=mapped_column(ForeignKey('interview_sessions.id')); order_index: Mapped[int]=mapped_column(Integer); text: Mapped[str]=mapped_column(Text); category: Mapped[str]=mapped_column(String(50)); difficulty: Mapped[str]=mapped_column(String(20)); expected_keywords: Mapped[list]=mapped_column(JSON,default=list); ideal_answer: Mapped[str]=mapped_column(Text,default=''); is_follow_up: Mapped[bool]=mapped_column(Boolean,default=False); source: Mapped[str]=mapped_column(String(20),default='bank')
class InterviewAnswer(Base):
    __tablename__='interview_answers'
    id: Mapped[int]=mapped_column(primary_key=True); session_id: Mapped[int]=mapped_column(ForeignKey('interview_sessions.id')); question_id: Mapped[int]=mapped_column(ForeignKey('interview_questions.id')); transcript: Mapped[str]=mapped_column(Text); input_mode: Mapped[str]=mapped_column(String(10)); duration_sec: Mapped[float]=mapped_column(Float,default=0); content_scores: Mapped[dict]=mapped_column(JSON,default=dict); speech_metrics: Mapped[dict]=mapped_column(JSON,default=dict); video_metrics: Mapped[dict]=mapped_column(JSON,default=dict); feedback: Mapped[dict]=mapped_column(JSON,default=dict); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class InterviewReport(Base):
    __tablename__='interview_reports'
    id: Mapped[int]=mapped_column(primary_key=True); session_id: Mapped[int]=mapped_column(ForeignKey('interview_sessions.id'),unique=True); overall_score: Mapped[float]=mapped_column(Float); category_scores: Mapped[dict]=mapped_column(JSON,default=dict); speech_summary: Mapped[dict]=mapped_column(JSON,default=dict); video_summary: Mapped[dict]=mapped_column(JSON,default=dict); strengths: Mapped[list]=mapped_column(JSON,default=list); weaknesses: Mapped[list]=mapped_column(JSON,default=list); suggestions: Mapped[list]=mapped_column(JSON,default=list); summary: Mapped[str]=mapped_column(Text,default=''); verdict: Mapped[str]=mapped_column(String(30)); trace: Mapped[list]=mapped_column(JSON,default=list); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

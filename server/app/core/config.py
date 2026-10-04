from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    PORT: int = 8000
    CLIENT_URL: str = 'http://localhost:5173'
    DATABASE_URL: str = 'sqlite:///./interviewiq.db'
    JWT_SECRET: str = 'development-secret-change-me'
    JWT_EXPIRES_MINUTES: int = 1440
    GEMINI_API_KEY: str = ''
    GEMINI_MODEL: str = 'gemini-2.0-flash'
    GROQ_API_KEY: str = ''
    GROQ_STT_MODEL: str = 'whisper-large-v3-turbo'
    EMBEDDING_MODEL: str = 'text-embedding-004'
    TTS_PROVIDER: str = 'browser'
    MAX_AUDIO_MB: int = 10
    SEED_SAMPLE_DATA: bool = True

settings = Settings()

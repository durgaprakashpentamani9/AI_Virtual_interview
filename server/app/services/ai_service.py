import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings

@retry(stop=stop_after_attempt(3),wait=wait_exponential(min=1,max=5),reraise=True)
async def generate(prompt: str) -> str | None:
    if not settings.GEMINI_API_KEY: return None
    url=f'https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}'
    async with httpx.AsyncClient(timeout=15) as client:
        res=await client.post(url,json={'contents':[{'parts':[{'text':prompt}]}],'generationConfig':{'responseMimeType':'application/json'}})
        res.raise_for_status(); return res.json()['candidates'][0]['content']['parts'][0]['text']

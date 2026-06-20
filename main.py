from fastapi import FastAPI
from config import settings
from datetime import datetime, timezone
import time
import httpx

from contextlib import asynccontextmanager
from database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🟢")
    init_db()  
    yield      
    print("🔴")

app=FastAPI(lifespan=lifespan)


START_TIME = time.time()


async def check_ollama() -> tuple[bool, str]:

    url = "http://localhost:11434/" 
    
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(url)
            
            if response.status_code == 200:
                return True, ""
            else:
                return False, f"model returned error: {response.status_code}"
            
    except Exception as e:
        return False, "model not available"
    
@app.get("/health")
async def health_check():

    uptime_sec = int(time.time() - START_TIME)
    
    is_ok, error_reason = await check_ollama()
    
    response = {
        "status": "ok" if is_ok else "degraded",
        "uptimeSec": uptime_sec,
        "backend": settings.backend,
        "model": settings.model,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    if not is_ok:
        response["reason"] = error_reason
        
    return response


@app.get("/model")
async def get_model_info():

    return {
        "backend": settings.backend,
        "model": settings.model,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens
    }
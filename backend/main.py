from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import tempfile
import os
from datetime import datetime
from typing import List, Optional
import uvicorn

# Local imports
from database import get_db, create_tables, get_or_create_user, User, TranscriptionLog, MemorizationStat
from auth import verify_firebase_token
from ml.transcriber import transcribe_audio
from ml.ayah_matcher import match_ayah

# Initialize FastAPI app
app = FastAPI(
    title="Dhikra API",
    description="Qur'an Memorization Assistant API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Pydantic models for requests/responses
class TranscribeResponse(BaseModel):
    transcription: str
    success: bool
    message: str

class MatchSentenceRequest(BaseModel):
    sentence: str

class MatchSentenceResponse(BaseModel):
    matched_ayah: Optional[str]
    similarity_score: float
    surah: Optional[int]
    ayah: Optional[int]
    arabic_text: str
    english_text: str
    success: bool

class TranscriptionLogResponse(BaseModel):
    id: str
    transcription_text: str
    matched_ayah: Optional[str]
    similarity_score: Optional[float]
    created_at: datetime

class MemorizationStatResponse(BaseModel):
    surah: int
    ayah: int
    times_attempted: int
    last_attempted: datetime

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()
    print("✅ Database tables created/verified")

@app.get("/")
async def root():
    return {"message": "Dhikra API is running", "version": "1.0.0"}

@app.post("/api/transcribe", response_model=TranscribeResponse)
async def transcribe_endpoint(
    audio: UploadFile = File(...),
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    """
    Transcribe audio file using Whisper
    """
    try:
        # Validate file type
        if not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Transcribe audio
            transcription = transcribe_audio(temp_file_path)
            
            return TranscribeResponse(
                transcription=transcription,
                success=True,
                message="Audio transcribed successfully"
            )
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.post("/api/match_sentence", response_model=MatchSentenceResponse)
async def match_sentence_endpoint(
    request: MatchSentenceRequest,
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    """
    Match a sentence to an ayah and log the result
    """
    try:
        # Get or create user
        user = get_or_create_user(db, firebase_uid)
        
        # Match ayah
        match_result = match_ayah(request.sentence)
        
        # Log transcription
        log_entry = TranscriptionLog(
            user_id=user.id,
            transcription_text=request.sentence,
            matched_ayah=match_result["matched_ayah"],
            similarity_score=match_result["similarity_score"]
        )
        db.add(log_entry)
        
        # Update or insert memorization stats
        if match_result["surah"] and match_result["ayah"]:
            existing_stat = db.query(MemorizationStat).filter(
                MemorizationStat.user_id == user.id,
                MemorizationStat.surah == match_result["surah"],
                MemorizationStat.ayah == match_result["ayah"]
            ).first()
            
            if existing_stat:
                existing_stat.times_attempted += 1
                existing_stat.last_attempted = datetime.utcnow()
            else:
                new_stat = MemorizationStat(
                    user_id=user.id,
                    surah=match_result["surah"],
                    ayah=match_result["ayah"],
                    times_attempted=1
                )
                db.add(new_stat)
        
        db.commit()
        
        return MatchSentenceResponse(
            matched_ayah=match_result["matched_ayah"],
            similarity_score=match_result["similarity_score"],
            surah=match_result["surah"],
            ayah=match_result["ayah"],
            arabic_text=match_result["arabic_text"],
            english_text=match_result["english_text"],
            success=True
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")

@app.get("/api/transcription_logs", response_model=List[TranscriptionLogResponse])
async def get_transcription_logs(
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """
    Get user's transcription history
    """
    try:
        user = get_or_create_user(db, firebase_uid)
        
        logs = db.query(TranscriptionLog).filter(
            TranscriptionLog.user_id == user.id
        ).order_by(TranscriptionLog.created_at.desc()).limit(limit).all()
        
        return [
            TranscriptionLogResponse(
                id=str(log.id),
                transcription_text=log.transcription_text,
                matched_ayah=log.matched_ayah,
                similarity_score=log.similarity_score,
                created_at=log.created_at
            )
            for log in logs
        ]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")

@app.get("/api/memorization_stats", response_model=List[MemorizationStatResponse])
async def get_memorization_stats(
    firebase_uid: str = Depends(verify_firebase_token),
    db: Session = Depends(get_db),
    surah: Optional[int] = None
):
    """
    Get user's memorization statistics
    """
    try:
        user = get_or_create_user(db, firebase_uid)
        
        query = db.query(MemorizationStat).filter(MemorizationStat.user_id == user.id)
        
        if surah:
            query = query.filter(MemorizationStat.surah == surah)
        
        stats = query.order_by(
            MemorizationStat.surah.asc(),
            MemorizationStat.ayah.asc()
        ).all()
        
        return [
            MemorizationStatResponse(
                surah=stat.surah,
                ayah=stat.ayah,
                times_attempted=stat.times_attempted,
                last_attempted=stat.last_attempted
            )
            for stat in stats
        ]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "dhikra-api"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 
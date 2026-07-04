from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import uvicorn
from datetime import datetime
import logging

from yinyang_dialectics import YinyangDialectics, APIKeyValidator, LicenseManager
from yinyang_dialectics.licensing import TierType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Yin-Yang Dialectics API",
    description="Recursive Adversarial Detection Engine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

validator = APIKeyValidator()

class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    max_depth: Optional[int] = Field(4, ge=1, le=8)
    return_detail: Optional[bool] = Field(False)

class AnalysisResponse(BaseModel):
    status: str
    yin_mass: int
    yang_resonance: int
    imbalance_ratio: float
    depth_reached: int
    is_adversarial: bool
    timestamp: str
    request_id: Optional[str] = None

async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")
    
    if not validator.validate(x_api_key):
        raise HTTPException(status_code=403, detail="Invalid or expired API key")
    
    is_allowed, usage_info = validator.check_rate_limit(x_api_key)
    if not is_allowed:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return x_api_key

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "operational",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }

@app.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze(
    request: AnalysisRequest,
    api_key: str = Depends(verify_api_key),
):
    try:
        validator.increment_usage(api_key)
        
        detector = YinyangDialectics(
            api_key=api_key,
            max_depth=request.max_depth,
            validate_key=False
        )
        
        result = detector.recursive_synthesis(request.text)
        
        return {
            **result,
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": api_key[:16],
        }
    
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/usage", tags=["Account"])
async def get_usage(api_key: str = Depends(verify_api_key)):
    _, usage_info = validator.check_rate_limit(api_key)
    
    return {
        "tier": usage_info.get("tier"),
        "current_usage": usage_info.get("current_usage"),
        "limit": usage_info.get("limit"),
        "remaining": usage_info.get("remaining"),
    }

@app.get("/tiers", tags=["Pricing"])
async def get_tiers():
    return LicenseManager.list_tiers()

@app.on_event("startup")
async def startup_event():
    logger.info("Yin-Yang Dialectics API started")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

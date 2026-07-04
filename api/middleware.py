from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
from typing import Dict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.request_log: Dict[str, list] = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = datetime.utcnow()
        
        if client_ip not in self.request_log:
            self.request_log[client_ip] = []
        
        self.request_log[client_ip] = [
            req_time for req_time in self.request_log[client_ip]
            if now - req_time < timedelta(hours=1)
        ]
        
        self.request_log[client_ip].append(now)
        
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = "100"
        response.headers["X-RateLimit-Remaining"] = str(100 - len(self.request_log[client_ip]))
        
        return response

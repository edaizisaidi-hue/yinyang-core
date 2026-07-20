from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from datetime import datetime
from collections import OrderedDict

class SovereignShieldMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_ip_capacity: int = 1000, max_payload_bytes: int = 4096):
        super().__init__(app)
        self.max_capacity = max_ip_capacity
        self.max_payload = max_payload_bytes
        self.request_log = OrderedDict()

    async def dispatch(self, request: Request, call_next):
        # 1. PRE-FLIGHT PAYLOAD SHIELD (Halang Bom Kognitif)
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_payload:
            return JSONResponse(
                status_code=413,
                content={"status": "rejected", "reason": "Payload exceeds sovereign threshold."}
            )

        # 2. ANTI-SPOOFING RATE LIMITER
        client_ip = request.client.host if request.client else "unknown"
        now = datetime.utcnow().timestamp()

        # Bounded Memory: Buang log lama jika kapasiti penuh
        if client_ip not in self.request_log and len(self.request_log) >= self.max_capacity:
            self.request_log.popitem(last=False)

        if client_ip not in self.request_log:
            self.request_log[client_ip] = []

        # Analisis halaju (60 saat terakhir)
        self.request_log[client_ip] = [
            req_time for req_time in self.request_log[client_ip]
            if now - req_time < 60
        ]

        if len(self.request_log[client_ip]) > 50:
            return JSONResponse(
                status_code=429,
                content={"status": "rejected", "reason": "Sovereign boundary rate-limit exceeded."}
            )

        self.request_log[client_ip].append(now)

        # 3. LALUAN BERSIH KEPADA ENJIN DFRYY
        response = await call_next(request)
        response.headers["X-Sovereign-Shield"] = "Active"
        return response

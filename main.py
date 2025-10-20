from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agora_token_builder import RtcTokenBuilder
import time
import os

app = FastAPI(title="Agora Token Generator")

# Load from environment or hardcode (better: use Render environment vars)
APP_ID = os.getenv("APP_ID", "YOUR_AGORA_APP_ID")
APP_CERTIFICATE = os.getenv("APP_CERTIFICATE", "YOUR_AGORA_APP_CERTIFICATE")
TOKEN_EXPIRE_SECONDS = int(os.getenv("TOKEN_EXPIRE_SECONDS", "3600"))  # 1 hour


# Request model
class TokenRequest(BaseModel):
channelName: str


@app.post("/api/channel/token")
def create_token(request: TokenRequest):
channel_name = request.channelName.strip()

if not channel_name:
raise HTTPException(status_code=400, detail="Channel name is required")

current_ts = int(time.time())
privilege_expired_ts = current_ts + TOKEN_EXPIRE_SECONDS

# UID = 0 → Agora assigns automatically
token = RtcTokenBuilder.build_token_with_uid(
APP_ID, APP_CERTIFICATE, channel_name, 0,
RtcTokenBuilder.Role_Publisher, privilege_expired_ts
)

return {
"channelName": channel_name,
"token": token,
"expireInSeconds": TOKEN_EXPIRE_SECONDS
}
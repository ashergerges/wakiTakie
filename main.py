from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import os

# ✳️ لاحظ هنا — الاستيراد من الكلاس الثاني
from agora_token_builder import RtcTokenBuilder2

app = FastAPI(title="Agora Token Generator")

APP_ID = os.getenv("APP_ID", "YOUR_AGORA_APP_ID")
APP_CERTIFICATE = os.getenv("APP_CERTIFICATE", "YOUR_AGORA_APP_CERTIFICATE")
TOKEN_EXPIRE_SECONDS = int(os.getenv("TOKEN_EXPIRE_SECONDS", "3600"))  # 1 hour


class TokenRequest(BaseModel):
    channelName: str


@app.post("/api/channel/token")
def create_token(request: TokenRequest):
    channel_name = request.channelName.strip()

    if not channel_name:
        raise HTTPException(status_code=400, detail="Channel name is required")

    current_ts = int(time.time())
    privilege_expired_ts = current_ts + TOKEN_EXPIRE_SECONDS

    try:
        # ✅ استخدام الكلاس الصحيح RtcTokenBuilder2
        token = RtcTokenBuilder2.build_token_with_uid(
            APP_ID,
            APP_CERTIFICATE,
            channel_name,
            0,  # UID
            RtcTokenBuilder2.Role_PUBLISHER,
            privilege_expired_ts,
        )

        return {
            "channelName": channel_name,
            "token": token,
            "expireInSeconds": TOKEN_EXPIRE_SECONDS,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating token: {str(e)}")

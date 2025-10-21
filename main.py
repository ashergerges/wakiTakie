from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agora_token_builder import RtcTokenBuilder
import time, os

app = FastAPI()

APP_ID = os.getenv("APP_ID", "your-agora-app-id")
APP_CERTIFICATE = os.getenv("APP_CERTIFICATE", "your-agora-app-cert")
TOKEN_EXPIRE_SECONDS = 3600


class TokenRequest(BaseModel):
    channelName: str


@app.post("/api/channel/token")
def create_token(request: TokenRequest):
    try:
        channel = request.channelName.strip()
        if not channel:
            raise HTTPException(status_code=400, detail="Missing channel name")

        uid = 0
        current_ts = int(time.time())
        expire = current_ts + TOKEN_EXPIRE_SECONDS

        token = RtcTokenBuilder.build_token_with_uid(
            APP_ID, APP_CERTIFICATE, channel, uid,
            RtcTokenBuilder.Role_PUBLISHER, expire
        )

        return {"channelName": channel, "token": token}
    except Exception as e:
        print("❌ Error:", e)
        raise HTTPException(status_code=500, detail=str(e))

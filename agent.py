import hmac
import hashlib
import os
import json
import logging
from typing import Optional

import httpx
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="Linear Agent Demo")

CLIENT_ID = os.getenv("LINEAR_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINEAR_CLIENT_SECRET")
WEBHOOK_SECRET = os.getenv("LINEAR_WEBHOOK_SECRET")
BASE_URL = os.getenv("BASE_URL")

TOKEN_STORE = "token.json"
REQUIRED_ENV_VARS = ["LINEAR_CLIENT_ID", "LINEAR_CLIENT_SECRET", "LINEAR_WEBHOOK_SECRET", "BASE_URL"]

missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


@app.get("/api/oauth/start")
async def oauth_start() -> RedirectResponse:
    """Start OAuth flow for Linear agent installation."""
    scopes = ["read", "write", "app:assignable", "app:mentionable"]
    auth_url = (
        "https://linear.app/oauth/authorize?"
        "response_type=code"
        f"&client_id={CLIENT_ID}"
        "&actor=app"
        f"&redirect_uri={BASE_URL}/api/oauth/callback"
        f"&scope={','.join(scopes)}"
    )
    return RedirectResponse(auth_url)

@app.get("/api/oauth/callback")
async def oauth_callback(code: str) -> str:
    """Handle OAuth callback and store access token."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.linear.app/oauth/token",
            data={
                "code": code,
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": f"{BASE_URL}/api/oauth/callback",
            },
        )
        
        if response.is_error:
            logger.error(f"OAuth token error: {response.status_code} - {response.text}")
            response.raise_for_status()
            
        # Store the token
        with open(TOKEN_STORE, "w") as f:
            f.write(response.text)
            
        logger.info("Successfully installed Linear agent")
        return "✅ Agent installed – you can assign it now."

def verify_webhook_signature(body: bytes, signature: str) -> bool:
    """Verify Linear webhook signature."""
    if not WEBHOOK_SECRET or not signature:
        return True
        
    calculated_sig = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, calculated_sig)

@app.post("/webhooks/linear")
async def handle_webhook(request: Request) -> dict:
    """Handle incoming Linear webhooks."""
    body = await request.body()
    signature = request.headers.get("linear-signature", "")
    
    # Verify webhook signature
    if not verify_webhook_signature(body, signature):
        logger.warning("Invalid webhook signature")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
    # Parse and process webhook payload
    payload = json.loads(body)
    event_type = payload.get("type")
    action = payload.get("action")
    
    if event_type == "AppUserNotification" and action in ("IssueAssigned", "IssueMentioned"):
        issue_title = payload["payload"]["issue"]["title"]
        logger.info(f"Received {action} notification for issue: {issue_title}")
    
    return {"ok": True}

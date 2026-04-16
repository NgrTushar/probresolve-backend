from collections.abc import AsyncGenerator
from typing import Optional
import uuid

from fastapi import Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.services.upload_service import _client as supabase_client


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_optional_user(request: Request) -> Optional[uuid.UUID]:
    """Extract and verify Supabase JWT if present."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
        
    token = auth_header.split(" ")[1]
    try:
        user_resp = supabase_client.auth.get_user(token)
        if user_resp and user_resp.user:
            return uuid.UUID(user_resp.user.id)
    except Exception as e:
        print(f"[AUTH ERROR] Supabase token verification failed: {e}")
        pass
    return None

async def get_current_user(request: Request) -> uuid.UUID:
    """Require authentication."""
    user_id = await get_optional_user(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user_id

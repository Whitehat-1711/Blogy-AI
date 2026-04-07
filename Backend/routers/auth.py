"""
POST /auth/signup and /auth/login.
Simple MongoDB-backed authentication for the frontend.
"""

from datetime import datetime
import hashlib
import hmac
import secrets

from fastapi import APIRouter, HTTPException

try:
    from Backend.models.request_models import SignupRequest, LoginRequest
    from Backend.core.database import get_users_collection
except ImportError:
    from ..models.request_models import SignupRequest, LoginRequest
    from ..core.database import get_users_collection


router = APIRouter(prefix="/auth", tags=["Authentication"])


def _normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def _hash_password(password: str, salt_hex: str | None = None) -> tuple[str, str]:
    salt = bytes.fromhex(salt_hex) if salt_hex else secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120000)
    return salt.hex(), digest.hex()


def _verify_password(password: str, salt_hex: str, digest_hex: str) -> bool:
    _, computed = _hash_password(password, salt_hex=salt_hex)
    return hmac.compare_digest(computed, digest_hex)


@router.post("/signup")
async def signup(req: SignupRequest):
    users = get_users_collection()
    if users is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    email = _normalize_email(req.email)
    existing = await users.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    salt, password_hash = _hash_password(req.password)
    now = datetime.utcnow()
    user_doc = {
        "username": req.username.strip(),
        "email": email,
        "password_hash": password_hash,
        "password_salt": salt,
        "created_at": now,
        "updated_at": now,
        "last_login_at": None,
    }
    result = await users.insert_one(user_doc)

    return {
        "success": True,
        "user": {
            "id": str(result.inserted_id),
            "username": user_doc["username"],
            "email": user_doc["email"],
        },
        "message": "Signup successful",
    }


@router.post("/login")
async def login(req: LoginRequest):
    users = get_users_collection()
    if users is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    email = _normalize_email(req.email)
    user = await users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not _verify_password(
        req.password,
        str(user.get("password_salt", "")),
        str(user.get("password_hash", "")),
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    await users.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login_at": datetime.utcnow(), "updated_at": datetime.utcnow()}},
    )

    return {
        "success": True,
        "user": {
            "id": str(user["_id"]),
            "username": user.get("username", ""),
            "email": user.get("email", ""),
        },
        "message": "Login successful",
    }


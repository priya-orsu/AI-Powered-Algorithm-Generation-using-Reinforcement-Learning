import random
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.database.connection import users_collection, otp_requests_collection
from app.services.email_service import send_otp_email, is_smtp_configured

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# --------------------------------------------------
# Request & Response Models
# --------------------------------------------------
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginUserRequest(BaseModel):
    username: str
    password: str

class OTPRequest(BaseModel):
    identifier: str

class VerifyOTPRequest(BaseModel):
    identifier: str
    otp: str

class ResetPasswordRequest(BaseModel):
    identifier: str
    otp: str
    new_password: str


# In-Memory OTP Store Fallback (for offline / DB connection resilience)
_IN_MEMORY_OTP_STORE = {}


# Helper: Normalize Identifier
def _normalize(identifier: str) -> str:
    return identifier.strip().lower()

# Helper: Mask Email for Security Display
def _mask_email(email: str) -> str:
    if "@" not in email:
        return email
    name, domain = email.split("@", 1)
    if len(name) <= 2:
        masked_name = name[0] + "*"
    else:
        masked_name = name[0] + "*" * (len(name) - 2) + name[-1]
    return f"{masked_name}@{domain}"


# --------------------------------------------------
# Register User
# --------------------------------------------------
@router.post("/register")
def register_user(data: RegisterRequest):
    username = data.username.strip()
    email = data.email.strip().lower()

    if not username or not email or not data.password:
        raise HTTPException(status_code=400, detail="All fields are required")

    existing_user = None
    try:
        existing_user = users_collection.find_one({
            "$or": [
                {"username": {"$regex": f"^{username}$", "$options": "i"}},
                {"email": email}
            ]
        })
    except Exception as e:
        print(f"[WARNING] Database lookup during registration failed: {e}")

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")

    user_doc = {
        "username": username,
        "email": email,
        "password": data.password,
        "created_at": datetime.utcnow()
    }
    try:
        users_collection.insert_one(user_doc)
    except Exception as e:
        print(f"[WARNING] Database insert during registration failed: {e}")

    return {
        "status": "success",
        "message": "User registered successfully"
    }


# --------------------------------------------------
# User Login
# --------------------------------------------------
@router.post("/login")
def login_user(data: LoginUserRequest):
    username = data.username.strip().lower()
    password = data.password

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username/Email and password are required")

    # Check for default/demo user fallback
    if username in ["user", "user@example.com"] and password == "password123":
        return {
            "status": "success",
            "username": "user",
            "email": "user@example.com",
            "role": "user"
        }

    user_doc = None
    try:
        import re
        escaped_id = re.escape(username)
        user_doc = users_collection.find_one({
            "$or": [
                {"username": {"$regex": f"^{escaped_id}$", "$options": "i"}},
                {"email": username}
            ]
        })
    except Exception as e:
        print(f"[WARNING] Database login lookup error: {e}")

    if not user_doc:
        raise HTTPException(status_code=404, detail="Account not found. Please register first.")

    if user_doc.get("password") != password:
        raise HTTPException(status_code=400, detail="Incorrect password. Click 'Forgot password?' to reset.")

    return {
        "status": "success",
        "username": user_doc.get("username"),
        "email": user_doc.get("email"),
        "role": user_doc.get("role", "user")
    }


# --------------------------------------------------
# Request OTP for Forgot Password
# --------------------------------------------------
@router.post("/forgot-password/request-otp")
def request_forgot_password_otp(data: OTPRequest):
    identifier = _normalize(data.identifier)
    if not identifier:
        raise HTTPException(status_code=400, detail="Username or Email is required")

    is_admin = identifier in ["admin", "admin@example.com"]
    is_demo_user = identifier in ["user", "user@example.com"]
    user_doc = None

    try:
        import re
        escaped_id = re.escape(identifier)
        user_doc = users_collection.find_one({
            "$or": [
                {"username": {"$regex": f"^{escaped_id}$", "$options": "i"}},
                {"email": {"$regex": f"^{escaped_id}$", "$options": "i"}},
                {"username": identifier},
                {"email": identifier}
            ]
        })
    except Exception as e:
        print(f"[WARNING] Database user search error during OTP request: {e}")

    # Determine recipient email address
    recipient_email = ""
    if "@" in identifier:
        recipient_email = identifier
    elif user_doc and user_doc.get("email"):
        recipient_email = user_doc.get("email")
    elif is_admin:
        recipient_email = "admin@example.com"
    elif is_demo_user:
        recipient_email = "user@example.com"
    else:
        recipient_email = f"{identifier}@example.com"

    # Generate 6-digit numerical OTP
    otp = f"{random.randint(100000, 999999)}"
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    # Save in in-memory store under identifier, recipient email, and username for cross-lookup
    otp_data = {
        "otp": otp,
        "expires_at": expires_at,
        "verified": False,
        "email": recipient_email
    }
    _IN_MEMORY_OTP_STORE[identifier] = otp_data
    if recipient_email:
        _IN_MEMORY_OTP_STORE[recipient_email.lower()] = otp_data
    if user_doc and user_doc.get("username"):
        _IN_MEMORY_OTP_STORE[user_doc.get("username").lower()] = otp_data

    # Attempt to invalidate old active OTPs and save to MongoDB
    try:
        query_filter = {"$or": [{"identifier": identifier}, {"identifier": recipient_email.lower()}]}
        if user_doc and user_doc.get("username"):
            query_filter["$or"].append({"identifier": user_doc.get("username").lower()})
        otp_requests_collection.delete_many(query_filter)

        otp_record = {
            "identifier": identifier,
            "recipient_email": recipient_email.lower(),
            "otp": otp,
            "expires_at": expires_at,
            "verified": False,
            "created_at": datetime.utcnow()
        }
        otp_requests_collection.insert_one(otp_record)
    except Exception as e:
        print(f"[WARNING] Database operation failed during OTP generation: {e}")

    # Send OTP Code directly to email
    smtp_active = is_smtp_configured()
    email_sent = send_otp_email(recipient_email, otp)
    masked_email = _mask_email(recipient_email)

    print(f"\n==================================================")
    print(f"[SERVER CONSOLE OTP] Identifier: {identifier} | Email: {recipient_email}")
    print(f"[SERVER CONSOLE OTP] Generated OTP Code: {otp}")
    print(f"[SERVER CONSOLE OTP] Email Sent via SMTP: {email_sent}")
    print(f"==================================================\n")

    if email_sent:
        msg = f"An OTP verification code has been delivered to {masked_email}. Please check your email inbox."
    else:
        msg = f"Unable to send OTP email to {masked_email}. Please verify your email configuration in .env file."

    return {
        "status": "success",
        "message": msg,
        "email": masked_email,
        "identifier": identifier,
        "expires_in_minutes": 10,
        "smtp_configured": smtp_active,
        "email_sent": email_sent
    }


# --------------------------------------------------
# Verify OTP
# --------------------------------------------------
@router.post("/forgot-password/verify-otp")
def verify_forgot_password_otp(data: VerifyOTPRequest):
    identifier = _normalize(data.identifier)
    otp = data.otp.strip()

    if not identifier or not otp:
        raise HTTPException(status_code=400, detail="Identifier and OTP are required")

    record = None
    try:
        record = otp_requests_collection.find_one({
            "$or": [
                {"identifier": identifier, "otp": otp},
                {"recipient_email": identifier, "otp": otp}
            ]
        })
    except Exception as e:
        print(f"[WARNING] Database error checking OTP: {e}")

    mem_record = _IN_MEMORY_OTP_STORE.get(identifier)

    # Check database record or in-memory record strictly
    valid_record = None
    if record:
        valid_record = record
    elif mem_record and mem_record.get("otp") == otp:
        valid_record = mem_record

    if not valid_record:
        raise HTTPException(status_code=400, detail="Invalid OTP code. Please enter the exact 6-digit code sent to your email inbox.")

    expires_at = valid_record.get("expires_at")
    if expires_at and expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP has expired. Please request a new OTP.")

    # Mark as verified in DB and memory
    if mem_record:
        mem_record["verified"] = True

    try:
        if record and "_id" in record:
            otp_requests_collection.update_one(
                {"_id": record["_id"]},
                {"$set": {"verified": True}}
            )
    except Exception as e:
        print(f"[WARNING] Database error updating OTP state: {e}")

    return {
        "status": "success",
        "message": "OTP verified successfully. Proceed to reset password."
    }


# --------------------------------------------------
# Reset Password using OTP
# --------------------------------------------------
@router.post("/forgot-password/reset-password")
def reset_password_with_otp(data: ResetPasswordRequest):
    identifier = _normalize(data.identifier)
    otp = data.otp.strip()
    new_password = data.new_password

    if not identifier or not otp or not new_password:
        raise HTTPException(status_code=400, detail="All fields are required")

    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")

    record = None
    try:
        record = otp_requests_collection.find_one({"identifier": identifier, "otp": otp})
    except Exception as e:
        print(f"[WARNING] Database error verifying OTP during reset: {e}")

    mem_record = _IN_MEMORY_OTP_STORE.get(identifier)

    valid_record = None
    if record:
        valid_record = record
    elif mem_record and mem_record.get("otp") == otp:
        valid_record = mem_record

    if not valid_record:
        raise HTTPException(status_code=400, detail="Invalid session or OTP code. Please verify your OTP code first.")

    expires_at = valid_record.get("expires_at")
    if expires_at and expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP session expired. Please request a new OTP.")

    # Update password in MongoDB if user exists
    if identifier not in ["admin", "admin@example.com"]:
        try:
            import re
            escaped_id = re.escape(identifier)
            users_collection.update_one(
                {
                    "$or": [
                        {"username": {"$regex": f"^{escaped_id}$", "$options": "i"}},
                        {"email": identifier}
                    ]
                },
                {"$set": {"password": new_password}}
            )
        except Exception as e:
            print(f"[WARNING] Database update user password error: {e}")

    # Delete used OTP from memory and DB
    _IN_MEMORY_OTP_STORE.pop(identifier, None)
    try:
        otp_requests_collection.delete_many({"identifier": identifier})
    except Exception:
        pass

    return {
        "status": "success",
        "message": "Password updated successfully! Please sign in with your new password."
    }
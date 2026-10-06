"""
SMTP Verification & Email Delivery Test Tool
--------------------------------------------
Run this script to verify your SMTP configuration in .env and send a test OTP email.

Usage:
    python test_smtp.py recipient@example.com
"""

import sys
import os
import random
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv(override=True)

from app.services.email_service import is_smtp_configured, send_otp_email

def main():
    print("=" * 60)
    print("      ALGORITHM GENERATOR - SMTP EMAIL TEST UTILITY      ")
    print("=" * 60)
    
    recipient = sys.argv[1] if len(sys.argv) > 1 else None
    
    smtp_host = os.getenv("SMTP_HOST", "").strip()
    smtp_port = os.getenv("SMTP_PORT", "").strip()
    smtp_user = os.getenv("SMTP_USER", "").strip()
    smtp_pass = os.getenv("SMTP_PASSWORD", "").strip()
    
    print(f"\n[1] Checking SMTP Settings from .env:")
    print(f"    - Host:     {smtp_host or '(Not set)'}")
    print(f"    - Port:     {smtp_port or '(Not set)'}")
    print(f"    - User:     {smtp_user or '(Not set)'}")
    print(f"    - Password: {'*' * len(smtp_pass) if smtp_pass else '(Not set)'}")
    
    if not is_smtp_configured():
        print("\n[!] STATUS: SMTP is NOT fully configured or is using default placeholders in .env.")
        print("\nTo send real OTP emails directly to user inboxes, please update your .env file:")
        print("    SMTP_HOST=smtp.gmail.com")
        print("    SMTP_PORT=587")
        print("    SMTP_USER=your_real_email@gmail.com")
        print("    SMTP_PASSWORD=your_16_character_app_password")
        print("    SMTP_FROM_EMAIL=your_real_email@gmail.com")
        print("\nNote for Gmail: Use a 16-character App Password generated from Google Account Security.")
        return

    print("\n[+] STATUS: SMTP configuration detected.")

    if not recipient:
        recipient = smtp_user

    print(f"\n[2] Attempting to send test OTP email to: {recipient}")
    test_otp = f"{random.randint(100000, 999999)}"
    
    success = send_otp_email(recipient, test_otp)
    
    if success:
        print(f"\n[+] SUCCESS: OTP email was successfully delivered to {recipient}!")
        print("    Check your inbox (and spam folder) for the verification email.")
    else:
        print(f"\n[-] ERROR: Failed to send email to {recipient}.")
        print("    Please verify your SMTP host, port, username, and password credentials.")

if __name__ == "__main__":
    main()

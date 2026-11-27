"""
Brevo Email Delivery Test Tool
-------------------------------
Run this script to test and verify your Brevo HTTP REST API configuration in .env.

Usage:
    python tests/test_brevo.py recipient@example.com
"""

import sys
import os
import random
from dotenv import load_dotenv

# Ensure root directory is in Python module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv(override=True)

from app.services.email_service import is_smtp_configured, send_otp_email, _send_via_brevo_api

def main():
    print("=" * 60)
    print("        ALGORITHM GENERATOR - BREVO EMAIL TEST UTILITY   ")
    print("=" * 60)
    
    recipient = sys.argv[1] if len(sys.argv) > 1 else None
    
    brevo_key = os.getenv("BREVO_API_KEY", "").strip()
    sender_email = os.getenv("BREVO_SENDER_EMAIL", "").strip() or "likithapriya2005@gmail.com"
    sender_name = os.getenv("BREVO_SENDER_NAME", "AlgoGen Studio").strip()
    
    masked_key = f"{brevo_key[:8]}...{brevo_key[-4:]}" if len(brevo_key) > 12 else ("(Not set)" if not brevo_key else "******")
    
    print("\n[1] Checking Brevo Configuration from .env:")
    print(f"    - BREVO_API_KEY:      {masked_key}")
    print(f"    - BREVO_SENDER_EMAIL: {sender_email}")
    print(f"    - BREVO_SENDER_NAME:  {sender_name}")
    
    if not brevo_key:
        print("\n[!] STATUS: BREVO_API_KEY is not set in .env.")
        print("\nTo send real OTP emails via Brevo directly to user inboxes:")
        print("  1. Sign in to your Brevo account at: https://app.brevo.com")
        print("  2. Generate an API Key under Settings -> SMTP & API -> API Keys:")
        print("     https://app.brevo.com/settings/keys/api")
        print("  3. Make sure your sender email is verified under Senders:")
        print("     https://app.brevo.com/senders")
        print("  4. Add the key to your .env file:")
        print("     BREVO_API_KEY=xkeysib-xxxxxxxxxxxxxxxxxxxx")
        print("     BREVO_SENDER_EMAIL=your_verified_brevo_email@gmail.com")
        return

    if not recipient:
        recipient = sender_email

    print(f"\n[2] Attempting to dispatch test OTP email via Brevo to: {recipient}")
    test_otp = f"{random.randint(100000, 999999)}"
    
    success = send_otp_email(recipient, test_otp)
    
    if success:
        print(f"\n[+] SUCCESS: Real OTP email ({test_otp}) was successfully delivered to {recipient} via Brevo!")
        print("    Check your inbox (and spam folder) for the verification email.")
    else:
        print(f"\n[-] ERROR: Failed to dispatch email via Brevo to {recipient}.")
        print("    Please check the error message above.")
        print(f"    Important: Ensure that '{sender_email}' is an approved sender in your Brevo account.")

if __name__ == "__main__":
    main()

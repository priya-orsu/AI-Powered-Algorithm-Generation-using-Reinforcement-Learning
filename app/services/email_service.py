import os
import smtplib
import logging
import json
import urllib.request
import urllib.error
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def is_smtp_configured() -> bool:
    """
    Checks if any valid email dispatch method (HTTP REST API or SMTP Credentials) is configured.
    """
    load_dotenv(override=True)
    
    # Check HTTP API Keys
    resend_key = os.getenv("RESEND_API_KEY", "").strip()
    brevo_key = os.getenv("BREVO_API_KEY", "").strip()
    sendgrid_key = os.getenv("SENDGRID_API_KEY", "").strip()
    if resend_key or brevo_key or sendgrid_key:
        return True

    # Check SMTP credentials
    smtp_host = os.getenv("SMTP_HOST", "").strip()
    smtp_user = os.getenv("SMTP_USER", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "").strip()
    
    if not (smtp_host and smtp_user and smtp_password):
        return False
        
    user_lower = smtp_user.lower()
    pass_lower = smtp_password.lower()
    
    placeholder_user_patterns = ["your_real_gmail_id@gmail.com", "your_email@gmail.com", "example.com"]
    placeholder_pass_patterns = ["your_16_character_app_password", "your_password", "placeholder"]
    
    if any(p in user_lower for p in placeholder_user_patterns):
        return False
    if any(p in pass_lower for p in placeholder_pass_patterns):
        return False
    return True


def _send_via_resend_api(api_key: str, recipient: str, subject: str, html_body: str) -> bool:
    """
    Sends email via Resend HTTP REST API (Port 443 HTTPS - No SMTP or App Password needed)
    """
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "AlgorithmGenerator/1.0"
    }
    payload = {
        "from": "Algorithm Generator <onboarding@resend.dev>",
        "to": [recipient],
        "subject": subject,
        "html": html_body
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status in (200, 201):
                logger.info(f"[RESEND REST API] Real OTP email successfully delivered to {recipient}")
                print(f"[RESEND REST API SUCCESS] Real OTP email delivered to {recipient}")
                return True
    except Exception as e:
        logger.error(f"[RESEND API ERROR] {e}")
        print(f"[RESEND API ERROR] Failed to send via Resend API: {e}")
    return False


def _send_via_brevo_api(api_key: str, recipient: str, subject: str, html_body: str) -> bool:
    """
    Sends email via Brevo HTTP REST API (Port 443 HTTPS - No SMTP needed)
    """
    url = "https://api.brevo.com/v3/smtp/email"
    sender_email = os.getenv("BREVO_SENDER_EMAIL", "").strip() or os.getenv("SMTP_FROM_EMAIL", "").strip() or os.getenv("SMTP_USER", "").strip() or "likithapriya2005@gmail.com"
    if "your_real" in sender_email or "example.com" in sender_email:
        sender_email = "likithapriya2005@gmail.com"

    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
        "User-Agent": "AlgorithmGenerator/1.0"
    }
    payload = {
        "sender": {"name": "Algorithm Generator", "email": sender_email},
        "to": [{"email": recipient}],
        "subject": subject,
        "htmlContent": html_body
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status in (200, 201):
                logger.info(f"[BREVO REST API] Real OTP email successfully delivered to {recipient}")
                print(f"[BREVO REST API SUCCESS] Real OTP email delivered to {recipient}")
                return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        logger.error(f"[BREVO API ERROR] HTTP {e.code}: {error_body}")
        print(f"[BREVO API ERROR] HTTP {e.code}: {error_body}")
    except Exception as e:
        logger.error(f"[BREVO API ERROR] {e}")
        print(f"[BREVO API ERROR] Failed to send via Brevo API: {e}")
    return False


def send_otp_email(recipient_email: str, otp_code: str) -> bool:
    """
    Dispatches a 6-digit OTP code to the recipient's email address using HTTP REST APIs or SMTP.
    """
    load_dotenv(override=True)
    
    subject = "Your Verification OTP Code - Algorithm Generator"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
        .container {{ max-width: 500px; margin: 0 auto; background: #1e293b; border-radius: 16px; border: 1px solid #334155; padding: 32px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5); }}
        .header {{ text-align: center; border-bottom: 1px solid #334155; padding-bottom: 20px; margin-bottom: 24px; }}
        .title {{ color: #38bdf8; font-size: 22px; font-weight: 700; margin: 0; }}
        .subtitle {{ color: #94a3b8; font-size: 14px; margin-top: 6px; }}
        .otp-box {{ background: #0f172a; border: 2px dashed #0284c7; border-radius: 12px; padding: 20px; text-align: center; margin: 24px 0; }}
        .otp-code {{ font-family: monospace; font-size: 36px; font-weight: 800; letter-spacing: 8px; color: #38bdf8; margin: 0; }}
        .expire-info {{ color: #f59e0b; font-size: 13px; font-weight: 600; margin-top: 10px; }}
        .body-text {{ font-size: 14px; line-height: 1.6; color: #cbd5e1; }}
        .warning {{ background: #451a03; border-left: 4px solid #f59e0b; padding: 12px 16px; border-radius: 4px; font-size: 12px; color: #fde68a; margin-top: 24px; }}
        .footer {{ text-align: center; margin-top: 32px; font-size: 12px; color: #64748b; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1 class="title">Algorithm Generator</h1>
          <p class="subtitle">Secure Password Reset Request</p>
        </div>
        <p class="body-text">Hello,</p>
        <p class="body-text">We received a request to reset the password for your account associated with <strong>{recipient_email}</strong>. Use the One-Time Password (OTP) code below to proceed:</p>
        
        <div class="otp-box">
          <h2 class="otp-code">{otp_code}</h2>
          <p class="expire-info">⏰ Valid for 10 minutes</p>
        </div>
        
        <p class="body-text">If you did not request a password reset, please ignore this email. Your account remains secure.</p>
        
        <div class="warning">
          <strong>Security Notice:</strong> Never share this OTP code with anyone. Our support team will never ask for your OTP.
        </div>
        
        <div class="footer">
          &copy; Algorithm Generator System &bull; Secure Authentication Service
        </div>
      </div>
    </body>
    </html>
    """

    # 1. Try Brevo HTTP REST API first if key exists (Unrestricted delivery to any email address)
    brevo_key = os.getenv("BREVO_API_KEY", "").strip()
    if brevo_key:
        if _send_via_brevo_api(brevo_key, recipient_email, subject, html_content):
            return True

    # 2. Try Resend HTTP REST API if key exists
    resend_key = os.getenv("RESEND_API_KEY", "").strip()
    if resend_key:
        if _send_via_resend_api(resend_key, recipient_email, subject, html_content):
            return True

    # 3. Try standard SMTP if configured
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "").strip()
    smtp_from = os.getenv("SMTP_FROM_EMAIL", "").strip() or smtp_user or "noreply@algorithmgenerator.com"
    smtp_tls = os.getenv("SMTP_TLS", "True").strip().lower() in ("true", "1", "yes")

    if not is_smtp_configured():
        print(f"[EMAIL SERVICE] No active HTTP API key or valid SMTP configuration in .env.")
        print(f"[EMAIL SERVICE SERVER CONSOLE] OTP Code for {recipient_email}: {otp_code}")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Algorithm Generator <{smtp_from}>"
        msg["To"] = recipient_email

        plain_text = f"Your Verification OTP Code for Algorithm Generator is: {otp_code}. Valid for 10 minutes."
        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10)
        elif smtp_tls:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
            server.starttls()
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)

        clean_password = smtp_password.replace(" ", "").strip()
        server.login(smtp_user, clean_password)
        server.sendmail(smtp_from, [recipient_email], msg.as_string())
        server.quit()
        logger.info(f"OTP Email successfully sent to {recipient_email}")
        print(f"[EMAIL SERVICE SUCCESS] Real OTP email delivered via SMTP to {recipient_email}")
        return True

    except Exception as e:
        logger.error(f"[EMAIL SERVICE ERROR] Failed to send email via SMTP to {recipient_email}: {e}")
        print(f"[EMAIL SERVICE ERROR] Failed to send email via SMTP to {recipient_email}: {e}")
        print(f"[EMAIL SERVICE SERVER CONSOLE] OTP Code for {recipient_email}: {otp_code}")
        return False

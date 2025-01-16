import random

def send_otp_via_whatsapp(phone_number):
    otp = random.randint(100000, 999999)
    # Logic to send OTP via WhatsApp (e.g., using Twilio or WhatsApp Business API)
    print(f"Sending OTP {otp} to {phone_number}")  # Debugging message
    return otp

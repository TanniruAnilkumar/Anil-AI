import smtplib
import threading
import speech_recognition as sr
from email.message import EmailMessage
from cryptography.fernet import Fernet

# === CONFIG ===
sender_email = "anilkumartanniru250@gmail.com"
receiver_email = "22jr5a0515@gmail.com"
password = "gqln ikqy qxaz rhke"  # Use env vars for security in real projects!

# Generate encryption key (save & reuse in real use cases)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def dictation_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Start dictating your email body. Speak clearly:")
        audio_data = recognizer.listen(source, timeout=10)
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"📝 You said: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"❌ Could not request results; {e}")
            return ""

def encrypt_text(text):
    return cipher_suite.encrypt(text.encode()).decode()

def send_email(body, subject="Anil AI Email with Features", attachment_path=None):
    encrypted_body = encrypt_text(body)
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(f"This is an encrypted message:\n\n{encrypted_body}\n\n(Decrypt with shared key)")

    if attachment_path:
        try:
            with open(attachment_path, "rb") as f:
                file_data = f.read()
                file_name = f.name
            msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
            print(f"📎 Attached file: {file_name}")
        except Exception as e:
            print(f"❌ Failed to attach file: {e}")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", e)

def schedule_email(delay_seconds, body, subject="Anil AI Email with Features", attachment_path=None):
    print(f"⏳ Scheduling email to be sent in {delay_seconds} seconds...")
    timer = threading.Timer(delay_seconds, send_email, args=(body, subject, attachment_path))
    timer.start()

if __name__ == "__main__":
    body = dictation_to_text()
    if not body:
        body = "Default email body because no dictation was captured."

    attachment = None  # e.g. "example.pdf" or None

    schedule_email(30, body, attachment_path=attachment)
    print("You can do other things now, your email will be sent automatically after 30 seconds.")

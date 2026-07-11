import os
import smtplib
import tomllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


PLACEHOLDER_VALUES = {
    "ornek_gonderen@gmail.com",
    "buraya_uygulama_sifresi_yazin",
    "ornek_alici@gmail.com",
}


def load_email_settings(base_dir=None):
    """`.streamlit/secrets.toml` dosyasindan e-posta ayarlarini oku ve dogrula."""
    base_dir = base_dir or os.path.abspath(os.path.dirname(__file__))
    secrets_path = os.path.join(base_dir, ".streamlit", "secrets.toml")

    if not os.path.exists(secrets_path):
        return None, f"Secrets dosyasi bulunamadi: {secrets_path}"

    try:
        with open(secrets_path, "rb") as f:
            secrets = tomllib.load(f)
    except Exception as exc:
        return None, f"Secrets dosyasi okunamadi: {exc}"

    settings = {
        "email_sender": str(secrets.get("EMAIL_SENDER", "")).strip(),
        "email_password": str(secrets.get("EMAIL_PASSWORD", "")).strip(),
        "email_receiver": str(secrets.get("EMAIL_RECEIVER", "")).strip(),
        "smtp_server": str(secrets.get("SMTP_SERVER", "smtp.gmail.com")).strip() or "smtp.gmail.com",
        "smtp_port": int(secrets.get("SMTP_PORT", 587)),
    }

    values_to_check = {
        settings["email_sender"],
        settings["email_password"],
        settings["email_receiver"],
    }

    if not all(values_to_check):
        return None, "E-posta ayarlari eksik. `.streamlit/secrets.toml` dosyasini doldurun."

    if values_to_check & PLACEHOLDER_VALUES:
        return None, "E-posta ayarlarinda hala ornek degerler var."

    return settings, ""


def send_email_message(subject, body, base_dir=None):
    """SMTP uzerinden UTF-8 e-posta gonder."""
    settings, error_message = load_email_settings(base_dir)
    if not settings:
        return False, error_message

    try:
        message = MIMEMultipart()
        message["From"] = settings["email_sender"]
        message["To"] = settings["email_receiver"]
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP(settings["smtp_server"], settings["smtp_port"]) as server:
            server.starttls()
            server.login(settings["email_sender"], settings["email_password"])
            server.sendmail(
                settings["email_sender"],
                settings["email_receiver"],
                message.as_string(),
            )

        return True, f"E-posta basariyla gonderildi: {settings['email_receiver']}"
    except Exception as exc:
        return False, f"E-posta gonderme hatasi: {exc}"

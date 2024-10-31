from flask_mail import Message
from flask import current_app

def trimite_notificare_email(nume_utilizator, email, produs_id, detalii):
    app = current_app
    mail = app.mail

    # Definirea mesajului de email
    mesaj = Message(subject="Cerere Nouă de Contact",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=['mihaihodis98@gmail.com'],  # adresa de email a administratorului
                    body=f"Nume: {nume_utilizator}\nEmail: {email}\nProdus ID: {produs_id}\nDetalii: {detalii}")
    
    # Trimiterea email-ului
    try:
        mail.send(mesaj)
    except Exception as e:
        print(f"Eroare la trimiterea email-ului: {e}")

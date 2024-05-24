import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(smtp_server, port, username, password, subject, html_template, recipients_file):
    with open(recipients_file, 'r') as file:
        recipients = [line.strip() for line in file]

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  
    server.login(username, password)

    for recipient in recipients:
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(html_template, 'html'))

        try:
            server.sendmail(username, recipient, msg.as_string())
            print(f"Email sent to {recipient}")
        except Exception as e:
            print(f"Failed to send email to {recipient}: {e}")

    server.quit()

def main():
    smtp_server = 'smtp.hostinger.com'  # SMTP sunucusu
    port = 587  # SMTP portu (Genellikle 587 veya 465)
    username = 'info@discoverwebtools.com'  # SMTP kullanıcı adı
    password = 'Furkeyan44/'  # SMTP şifresi
    subject = 'Your Subject Here'  # E-posta konusu
    html_template = """
    <html>
    <body>
        <h1>This is a test email</h1>
        <p>This is a paragraph in the test email.</p>
    </body>
    </html>
    """  # HTML e-posta şablonu
    recipients_file = 'recipients.txt'  # Alıcıların bulunduğu dosya

    send_email(smtp_server, port, username, password, subject, html_template, recipients_file)

if __name__ == "__main__":
    main()

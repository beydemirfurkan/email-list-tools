import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import webbrowser
import tempfile

# E-posta gönderim fonksiyonu
def send_email(smtp_server, port, username, password, subject, html_template, recipients_file):
    try:
        with open(recipients_file, 'r') as file:
            recipients = [line.strip() for line in file]

        # SMTP sunucusuna bağlan
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
                status_text.insert(tk.END, f"Email sent to {recipient}\n")
            except Exception as e:
                print(f"Failed to send email to {recipient}: {e}")
                status_text.insert(tk.END, f"Failed to send email to {recipient}: {e}\n")

        server.quit()
        messagebox.showinfo("Success", "Emails have been sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Alıcı dosyasını seçme fonksiyonu
def select_recipients_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    entry_recipients_file.delete(0, tk.END)
    entry_recipients_file.insert(0, file_path)

# HTML şablonunu doğrulama ve önizleme fonksiyonu
def preview_html():
    html_template = text_html_template.get("1.0", tk.END)
    
    # Geçici bir dosya oluşturup HTML'yi yazalım ve tarayıcıda açalım
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as temp_file:
        temp_file.write(html_template)
        webbrowser.open(f"file://{temp_file.name}")

# E-posta gönderim işlemini başlatma fonksiyonu
def send_emails():
    smtp_server = entry_smtp_server.get()
    port = int(entry_port.get())
    username = entry_username.get()
    password = entry_password.get()
    subject = entry_subject.get()
    html_template = text_html_template.get("1.0", tk.END)
    recipients_file = entry_recipients_file.get()

    if not smtp_server or not port or not username or not password or not subject or not recipients_file:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    send_email(smtp_server, port, username, password, subject, html_template, recipients_file)

# Tkinter ana penceresini oluşturma
root = tk.Tk()
root.title("Bulk Email Sender")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

# SMTP Sunucusu ve Port Bilgileri
label_smtp_server = tk.Label(frame, text="SMTP Server:")
label_smtp_server.grid(row=0, column=0, padx=10, pady=5)
entry_smtp_server = tk.Entry(frame, width=50)
entry_smtp_server.grid(row=0, column=1, padx=10, pady=5)

label_port = tk.Label(frame, text="Port:")
label_port.grid(row=1, column=0, padx=10, pady=5)
entry_port = tk.Entry(frame, width=50)
entry_port.grid(row=1, column=1, padx=10, pady=5)

# SMTP Kullanıcı Adı ve Şifre
label_username = tk.Label(frame, text="Username (Email):")
label_username.grid(row=2, column=0, padx=10, pady=5)
entry_username = tk.Entry(frame, width=50)
entry_username.grid(row=2, column=1, padx=10, pady=5)

label_password = tk.Label(frame, text="Password:")
label_password.grid(row=3, column=0, padx=10, pady=5)
entry_password = tk.Entry(frame, width=50, show="*")
entry_password.grid(row=3, column=1, padx=10, pady=5)

# E-posta Konusu
label_subject = tk.Label(frame, text="Email Subject:")
label_subject.grid(row=4, column=0, padx=10, pady=5)
entry_subject = tk.Entry(frame, width=50)
entry_subject.grid(row=4, column=1, padx=10, pady=5)

# Alıcı Dosyası Seçimi
label_recipients_file = tk.Label(frame, text="Recipients File (TXT):")
label_recipients_file.grid(row=5, column=0, padx=10, pady=5)
entry_recipients_file = tk.Entry(frame, width=50)
entry_recipients_file.grid(row=5, column=1, padx=10, pady=5)
button_recipients_file = tk.Button(frame, text="Browse", command=select_recipients_file, bg="black", fg="white")
button_recipients_file.grid(row=5, column=2, padx=10, pady=5)

# HTML Şablonu Girişi
label_html_template = tk.Label(frame, text="HTML Template:")
label_html_template.grid(row=6, column=0, padx=10, pady=5)
text_html_template = tk.Text(frame, width=50, height=10)
text_html_template.grid(row=6, column=1, padx=10, pady=5, columnspan=2)

# HTML Şablonu Önizleme Butonu
button_preview = tk.Button(frame, text="Preview HTML", command=preview_html, bg="black", fg="white")
button_preview.grid(row=7, column=0, padx=10, pady=5)

# Gönderim Durumları/Loglar
label_status = tk.Label(frame, text="Status/Logs:")
label_status.grid(row=9, column=0, padx=10, pady=5)
status_text = scrolledtext.ScrolledText(frame, width=50, height=10)
status_text.grid(row=9, column=1, padx=10, pady=5, columnspan=2)

# E-posta Gönder Butonu
button_send = tk.Button(frame, text="Send Emails", command=send_emails, bg="black", fg="white")
button_send.grid(row=10, column=1, pady=20)

# Tkinter ana döngüsü
root.mainloop()

import smtplib
from email.mime.text import MIMEText

def send_gmail(gmail_account, gmail_password, to_email, subject, body):
    # GmailのSMTPサーバーの情報
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # TLSでの接続に必要なポート番号

    # MIMETextオブジェクトの作成
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = gmail_account
    msg['To'] = to_email

    # GmailのSMTPサーバーに接続
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail_account, gmail_password)
    server.send_message(msg)
    server.quit()


def run():
    # 関数の呼び出し
    # send_gmail("your_account@gmail.com", "your_password", "to@example.com", "Test mail", "This is a test mail.")

    login_account="woxram@gmail.com"
    app_password="kitxptpvlytwvyxq"
    to_email="ma3hi68rada@gmail.com"
    title="Test mail"
    body="This is woxram server"

    send_gmail(login_account, app_password, to_email, title, body)


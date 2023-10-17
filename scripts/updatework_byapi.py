from app1.models import VoiceDataModel
from utility.utils import AddWorkAPI

import amadeus

import requests,time,datetime

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
    queryset=VoiceDataModel.objects.filter(id__range=(7000, 10000))
    # queryset=VoiceDataModel.objects.filter(id=2000)
    fail_ids=[]

    for record in queryset:
        time.sleep(5)
        print('@@@@@@@@@@@@@@@@@@@@@@@')
        if(record.text_version!="posted_script"):
            with open('tmp/update_work_history.txt','a',encoding='utf-8') as f:
                f.write('id:{0} date:{1}\n'.format(record.id,datetime.datetime.now()))
            work_id=record.work_id.split('x')[0]
            print('id:{0} work_id:{1} をを更新作業中'.format(record.id,work_id))
            url='http://133.130.96.237/api/transcript/getdlsite2/?work_id={0}'.format(work_id)
            print(url+'にアクセス開始')
            try:
                response=requests.get(url).json()
            except:
                print("woxram api サーバに再接続します")
                time.sleep(60)
                response=requests.get(url).json()
            
            if(response["status_code"]==200):
                addwork=AddWorkAPI(response)
                addwork.update_sample_records()
            else:
                with open('tmp/fail_ids.txt','a',encoding='utf-8') as f:
                    f.write("id:{0} url:{1}\n".format(record.id,record.url))

        else:
            print("id : {0} is posted_script".format(record.id))



    login_account="woxram@gmail.com"
    app_password="kitxptpvlytwvyxq"
    to_email="ma3hi68rada@gmail.com"
    title="Addwork_byapi is done."
    body="Addwork_byapi is done."

    send_gmail(login_account, app_password, to_email, title, body)




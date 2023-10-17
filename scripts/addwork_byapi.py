from app1.models import VoiceDataModel
from utility.utils import AddWorkAPI

import requests, json, os, sys,time

import smtplib
from email.mime.text import MIMEText

import amadeus

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
    if(os.path.isfile('tmp/workurls_tmp.txt')):
        with open('tmp/workurls_tmp.txt','r',encoding='utf-8') as f:
            workurls=(f.read()).split(',')
    else:
        workurls=amadeus.DlsiteTools().get_workurls(2023,10,7)

    # 手動
    # workurls=["https://www.dlsite.com/maniax/work/=/product_id/RJ010101.html"]

    print(workurls)
    with open('tmp/workurls_tmp.txt','w',encoding='utf-8') as f:
        f.write(','.join(workurls))


    for workurl in workurls:
        time.sleep(3)
        print('@@@@@@@@@@@@@@@@@@@@@@@')
        work_id=workurl.split('/')[-1].split('.')[0]
        print(work_id+' を登録作業中')
        workinfo=amadeus.WorkInfo(workurl)
        if('ボイス・ASMR' in workinfo.type):
            if(workinfo.lang==[] or ('日本語' in workinfo.lang)):
                url='http://133.130.96.237/api/transcript/getdlsite2/?work_id={0}'.format(work_id)
                print(url+'にアクセス開始')
                try:
                    response=requests.get(url).json()
                except:
                    print("woxram api サーバに再接続します")
                    time.sleep(60)
                    response=requests.get(url).json()
                
                addwork=AddWorkAPI(response)
                addwork.update_sample_records()
            else:
                print(work_id+'は日本語作品じゃない')
        else:
            print(work_id+'はボイス・ASMR 作品じゃない')

    login_account="woxram@gmail.com"
    app_password="kitxptpvlytwvyxq"
    to_email="ma3hi68rada@gmail.com"
    title="Addwork_byapi is done."
    body="Addwork_byapi is done."

    send_gmail(login_account, app_password, to_email, title, body)

    os.remove('tmp/workurls_tmp.txt')



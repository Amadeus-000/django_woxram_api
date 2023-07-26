import requests
from app1.models import VoiceDataModel

def run():

    # print("runscript")

    # response=requests.get('http://133.130.96.237/api/transcript/test')
    # print(response.text)

    records=VoiceDataModel.objects.all()
    records=records.filter(maintext__contains='\r')
    for r in records:
        print(r.id)
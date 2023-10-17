import requests
from app1.models import VoiceDataModel
import amadeus

def run():

    print("runscript")

    # response=requests.get('http://133.130.96.237/api/transcript/test')
    # print(response.text)

    workinfo=amadeus.WorkInfo('https://www.dlsite.com/maniax/work/=/product_id/RJ01049007.html')
    print(workinfo.title)


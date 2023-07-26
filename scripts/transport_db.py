from account.models import MemoData
from api1.models import SearchExample
from app1.models import CharacterVoiceModel,CircleModel,ScenarioWriterModel,VoiceDataModel

import requests
import json
import random
import string

def generate_random_string(length):
    # 英字(大文字と小文字)と数字のリストを作成
    characters = string.ascii_letters + string.digits
    
    # 指定された長さのランダムな文字列を生成
    random_string = ''.join(random.choice(characters) for i in range(length))
    
    return random_string

def run():
    print("start")
    # for i in range(0,2760+1):
    #     print("id:{0}".format(i))
    #     addCV(i)

    # for i in range(0,2761+1):
    #     print("id:{0}".format(i))
    #     addSW(i)

    # for i in range(0,2212+1):
    #     print("id:{0}".format(i))
    #     addCircle(i)

    # for i in range(0,29118+1):
    #     print("id:{0}".format(i))
    #     addVoicedata(i)

    for i in range(0,127+1):
        print("id:{0}".format(i))
        addMemodata(i)

    for i in range(0,38+1):
        print("id:{0}".format(i))
        addSearchExample(i)

    # addMemodata(10)
    # addSearchExample(10)
    # addCircle(2212)
    # addCV(10)
    # addSW(10)
    # addVoicedata(232)

    # query=CircleModel.objects.filter(circle_id="RG65522")
    # for q in query:
    #     print(q.id)
    #     print(q.circle)


def addMemodata(id_input):
    url="https://woxram-api.com/db/memodata/?id={0}".format(id_input)
    response=requests.get(url).json()
    print(response)
    if(response):
        obj=MemoData(
            public_id=response["public_id"],
            public_record_id=response["public_record_id"],
            info=response["info"],
            chapter_name=response["chapter_name"],
            text=response["text"],
        )
        obj.save()

def addSearchExample(id_input):
    url="https://woxram-api.com/db/searchexample/?id={0}".format(id_input)
    response=requests.get(url).json()
    print(response)
    if(response):
        obj=SearchExample(
            url=response["url"],
            keyword=response["keyword"],
        )
        obj.save()

def addCircle(id_input):
    url="https://woxram-api.com/db/circle/?id={0}".format(id_input)
    response=requests.get(url).json()
    print(response)

    if(response):
        if(response["name"]=="八朔あかりのうらあか"):
            return 0
        obj=CircleModel(
            circle=response["name"],
            yomigana="00000",
            circle_id=response["id"],
            url_circle=response["url"],
            publication_state="",
            approval_state="未許可",
            supplement="",
        )
        obj.save()
    
def addCV(id_input):
    url="https://woxram-api.com/db/cv/?id={0}".format(id_input)
    response=requests.get(url).json()
    print(response)
    if(response):
        obj=CharacterVoiceModel(
            character_voice=response["name"],
            yomigana="00000",
            cv_id=generate_random_string(25)
        )
        obj.save()
        obj.cv_id="cv{0}".format(obj.id)
        obj.save()

def addSW(id_input):
    url="https://woxram-api.com/db/sw/?id={0}".format(id_input)
    response=requests.get(url).json()
    print(response)
    if(response):
        obj=ScenarioWriterModel(
            scenario_writer=response["name"],
            yomigana="00000",
            sw_id=""
        )
        obj.save()
        obj.sw_id="sw{0}".format(obj.id)
        obj.save()

def addVoicedata(id_input):
    url="https://woxram-api.com/db/voicedata/?id={0}".format(id_input)
    response=requests.get(url).json()
    print(response)
    if(response):
        circle_obj=CircleModel.objects.get(circle_id=response["circle_id"])
        obj=VoiceDataModel(
            public_record_id=response["public_record_id"],
            name=response["name"],
            work_id=response["work_id"],
            circle=circle_obj,
            release_date=response["release_date"],
            add_date=response["add_date"],
            url=response["url"],
            url_af="",
            url_img=response["url_img"],
            commerce_switch=True,
            public_switch=response["public_switch"],
            public_delete=response["public_delete"],
            sample_switch=response["sample_switch"],
            adult_switch=response["adult_switch"],
            confidence=0,
            display_range=100,
            description=response["description"],
            description_original=response["description_original"],
            description_conv=response["description_conv"],
            chapter_names=response["chapter_names"],
            maintext_original=response["maintext_original"],
            maintext=response["maintext"],
            maintext_conv=response["maintext_conv"],
            maintext_old=response["maintext_old"],
            text_version=response["text_version"],
        )
        obj.save()

        for cv in response["character_voice"]:
            cv_obj=CharacterVoiceModel.objects.get(character_voice__exact=cv)
            obj.character_voice.add(cv_obj)
        
        for sw in response["scenario_writers"]:
            sw_obj=ScenarioWriterModel.objects.get(scenario_writer=sw)
            obj.scenario_writers.add(sw_obj)
        
        obj.save()

# モデル
from app1.models import VoiceDataModel, CircleModel, CharacterVoiceModel,ScenarioWriterModel,OrderMenu,GenreModel,WorkTextState

# モジュール
import datetime, time, os, sys,jaconv

# エラー
from django.db.utils import OperationalError

import amadeus



class AddWorkAPI:
    def __init__(
            self,
            workinfo,
            commerce_switch=True,
            sample_switch=True,
            public_switch=True,
            display_range=100,
            create_user=''
        ):
        self.workinfo=workinfo

        #発売日のチェック
        if(self.workinfo["release_date"]=='-'):
            self.workinfo["release_date"]='2000年01月01日'

        #アダルトコンテンツ
        if(self.workinfo["adult"]=='18禁'):
            self.adult_switch=True
        else:
            self.adult_switch=False

        self.commerce_switch=commerce_switch
        self.sample_switch=sample_switch
        self.public_switch=public_switch
        self.display_range=display_range
        self.create_user=create_user

    def make_sample_records(self):

        # descriptionの準備
        descripton_info='{0}\n{1}\n{2}\n{3}'.format(self.workinfo["title"],self.workinfo["circle"],'/'.join(self.workinfo["cv"]),'/'.join(self.workinfo["scenario"]))
        description=descripton_info+'\n\n'+self.workinfo["description"]
        modify_text_des=amadeus.ModifyText(description)
        description=modify_text_des.text
        description_conv=modify_text_des.text_conv

        obj=VoiceDataModel(
            name=self.workinfo["title"],
            circle=self.check_create__rename_cir(self.workinfo["circle"],self.workinfo["circle_url"]),
            url=self.workinfo["url"],
            url_img=self.workinfo["imgurl"],
            release_date=self.date_conv(self.workinfo["release_date"]),
            commerce_switch=self.commerce_switch,
            public_switch=self.public_switch,
            sample_switch=self.sample_switch,
            adult_switch=self.adult_switch,
            display_range=self.display_range,
            confidence=100.0,
            work_id=self.workinfo["work_id"]+'xs',
            description_original=self.workinfo["description"],
            description=description,
            description_conv=description_conv,
            chapter_names='ΦΦΦΦΦ'.join(self.workinfo["chapter_names"]),
            maintext_original='ΦΦΦΦΦ'.join(self.workinfo["maintext_original"]),
            maintext='ΦΦΦΦΦ'.join(self.workinfo["maintext"]),
            maintext_conv='ΦΦΦΦΦ'.join(self.workinfo["maintext_conv"]),
            text_version=self.workinfo["text_version"],
        )

        self.save_record_retry(obj)

        #声優、シナリオ　を追加
        for x in self.workinfo["cv"]:
            obj.character_voice.add( self.check_create_cv(x) )
        for x in self.workinfo["scenario"]:
            obj.scenario_writers.add( self.check_create_sw(x) )

        if(self.create_user!=''):
            obj.create_user=self.create_user
        
        self.save_record_retry(obj)

        print("id={0} recordが作成されました".format(obj.id))

    def update_sample_records(self):
        if(VoiceDataModel.objects.filter(work_id=self.workinfo['work_id']+'xs').exists()):
            record=VoiceDataModel.objects.get(work_id=self.workinfo['work_id']+'xs')

            # descriptionの準備
            descripton_info='{0}\n{1}\n{2}\n{3}'.format(self.workinfo["title"],self.workinfo["circle"],'/'.join(self.workinfo["cv"]),'/'.join(self.workinfo["scenario"]))
            description=descripton_info+'\n\n'+self.workinfo["description"]
            modify_text_des=amadeus.ModifyText(description)
            description=modify_text_des.text
            description_conv=modify_text_des.text_conv

            record.description_original=self.workinfo["description"]
            record.description=description
            record.description_conv=description_conv

            record.name=self.workinfo["title"]
            record.add_date=datetime.date.today()
            record.chapter_names='ΦΦΦΦΦ'.join(self.workinfo["chapter_names"])
            record.maintext_original='ΦΦΦΦΦ'.join(self.workinfo["maintext_original"])
            record.maintext='ΦΦΦΦΦ'.join(self.workinfo["maintext"])
            record.maintext_conv='ΦΦΦΦΦ'.join(self.workinfo["maintext_conv"])
            record.text_version=self.workinfo["text_version"]

            #声優、シナリオ　を追加
            record.character_voice.clear()
            for x in self.workinfo["cv"]:
                record.character_voice.add( self.check_create_cv(x) )
            record.scenario_writers.clear()
            for x in self.workinfo["scenario"]:
                record.scenario_writers.add( self.check_create_sw(x) )

            self.save_record_retry(record)
            print("id={0} recordがupdateされました".format(record.id))
        else:
            self.make_sample_records()

    def check_create__rename_cir(self,cir_name_input,cir_url_input):
        cir_id_input=(cir_url_input.split('/')[-1]).split('.')[0]
        query=CircleModel.objects.all()
        if(query.filter(circle_id=cir_id_input).exists()):
            record=query.get(circle_id=cir_id_input)
            if(record.circle!=cir_name_input):
                record.supplement='{0}\nold name : {1}\n'.format(record.supplement, record.circle)
                record.circle=cir_name_input
                record.alias=cir_name_input
                record.save()
                print('{0} id={1} is renamed.'.format(record.circle,record.id))
        else:
            record=CircleModel(
                circle=cir_name_input,
                yomigana='00000',
                alias=cir_name_input.replace(' ', '_'),
                circle_id=cir_id_input,
                url_circle=cir_url_input,
            )
            record.save()
            print('circle : {0} is created.'.format(cir_name_input))
        return record
    def check_create_cv(self,cv_name_input):
        #入力された声優がデータベースに存在するかチェックして、存在しない場合は作成する
        #入力された声優のオブジェクトを返す
        query=CharacterVoiceModel.objects.all()
        existornot=query.filter(character_voice=cv_name_input).exists()
        # print(existornot)
        if(not existornot):
            obj=CharacterVoiceModel(
                character_voice=cv_name_input,
                yomigana='00000',
                alias=cv_name_input,
            )
            obj.save()
            print('creating '+cv_name_input)
        obj=query.get(character_voice=cv_name_input)
        return obj
    def check_create_sw(self,sw_name_input):
        #入力された声優がデータベースに存在するかチェックして、存在しない場合は作成する
        #入力された声優のオブジェクトを返す
        query=ScenarioWriterModel.objects.all()
        existornot=query.filter(scenario_writer=sw_name_input).exists()
        # print(sw_name_input)
        # print('このシナリオライターはScenarioWriterModelに存在するか : {0}'.format(existornot))
        if(not existornot):
            obj=ScenarioWriterModel(
                scenario_writer=sw_name_input,
                yomigana='00000',
                alias=sw_name_input,
            )
            obj.save()
            print('creating '+sw_name_input)
        obj=query.get(scenario_writer=sw_name_input)
        return obj
    def save_record_retry(self,record):
        # レコード保存、データベースがロックされているときはリトライ
        try:
            record.save()
        except OperationalError:
            print('retry save...')
            time.sleep(30)
            record.save()

    def on2true(self,input):
        if(input=='on'):
            return True
        elif(input==True):
            return True
        elif(input=='off'):
            return False
        else:
            return False
    def date_conv(self,date_input):
        year=int(date_input.split('年')[0])
        date_input=date_input.split('年')[1]
        month=int(date_input.split('月')[0])
        date_input=date_input.split('月')[1]
        day=int(date_input.split('日')[0])

        return datetime.date(year, month, day)

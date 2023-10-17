import time,random,os,sys,time, json,random
import jaconv,re,copy, datetime, itertools
from django.db.models import Q
from django.db.models import Case, When, Value, IntegerField
from django.core.exceptions import ObjectDoesNotExist

import base64

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from app1.models import CircleModel, CharacterVoiceModel, ScenarioWriterModel, VoiceDataModel, SearchLog
from account.models import MemoData
from .models import SearchExample

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

import amadeus

class CheckDatabaseUpdateInfo(APIView):
    def get(self,request):
        return Response("データベース更新日 2023/10/14")


class GetNamelist_ccs(APIView):
    def get(self,request):
        testlist=['ocelot','snake','raiden','佐藤','秋野かえで']
        namelist=[]
        queryset=CircleModel.objects.all()
        for q in queryset:
            namelist.append(q.circle)
        queryset=CharacterVoiceModel.objects.all()
        for q in queryset:
            namelist.append(q.character_voice)
        queryset=ScenarioWriterModel.objects.all()
        for q in queryset:
            namelist.append(q.scenario_writer)
        return Response(list(set(namelist)))

class GetCircleId(APIView):
    def get(self,request):
        circle_id=[]
        queryset=CircleModel.objects.all()
        for i in queryset:
            circle_id.append(i.circle_id)
        return Response(circle_id)


@method_decorator(never_cache, name='dispatch')
class RandSearchExample(APIView):
    def get(self,request):
        all_records=list(SearchExample.objects.all())
        random_records_10 = random.sample(all_records,10)
        return Response([(i.keyword, i.url) for i in random_records_10])
        

class WoxramSearchAPI(APIView):
    def get(self,request):
        start_time=time.time()
        if(request.GET.get('keyword',False)):
            request_post=request.GET
            si_ins=SearchInfo(request_post)

            page=int(request.GET.get('page',1))

            wis_ins=WorkInfoSearch(si_ins.dlsite_sch)
            #必須じゃないフィルター
            if(request.GET.get('safe')=='on'):
                wis_ins.filter_adult(False)
            wis_ins.filter_sample(si_ins.sample_switch)
            wis_ins.filter_public(True)
            wis_ins.filter_circle(si_ins.circle_checkbox)
            wis_ins.filter_cv(si_ins.character_voice_checkbox)
            wis_ins.filter_scenario(si_ins.scenario_checkbox)
            wis_ins.filter_genre(si_ins.genres_checkbox)
            #必須のフィルター
            wis_ins.set_keywords(si_ins.joined_keywords)

            #並び替え、データの成形
            wis_ins.sort_queryset(si_ins.order_input)
            wis_ins.search_keyword6(page)
            results_works=wis_ins.results_works
            number_of_record=wis_ins.number_of_record
            
            end_time=time.time()

            obj=SearchLog(
                keyword=request.GET.get('keyword','home'),
                elapsed_time=end_time-start_time,
            )
            obj.save()
        elif(request.GET.get('memo',False)):
            wis_ins=WorkInfoSearch()
            memo=request.GET.get('memo',False)
            if(memo[0:4]=='memo'):
                results_works=wis_ins.search_from_memo_database(memo)
            else:
                results_works=wis_ins.search_from_memo(memo)
            return Response([results_works,1])

        # return Response(results_works)
        return Response([results_works,number_of_record])

class GetMaintext(APIView):
    def get(self,request):
        id_input=request.GET.get("id")
        records=VoiceDataModel.objects.filter(id=id_input)
        if(records.exists()):
            for record in records:
                return Response({
                    "work_id":record.work_id,
                    "maintext":record.maintext,
                })
        else:
            return Response(False)

class WorkInfoSearch:
    def __init__(self,dlsite_sch=False):
        # self.queryset=VoiceDataModel.objects.all()
        self.queryset=VoiceDataModel.objects.defer('maintext_old','genres','confidence','maintext_original','description_original')
        self.Xjoin_char=r'[、。… \?]*'
        self.dlsite_sch=dlsite_sch

    def filter_user(self,user):
        pass
    def filter_sample(self,input_sm):
        if(input_sm==False):
            self.queryset=self.queryset.filter(sample_switch=input_sm)
        return self.queryset
    def filter_public(self,input_pub):
        if(input_pub):
            self.queryset=self.queryset.filter(public_switch=input_pub)
        return self.queryset
    def filter_adult(self,input_ad):
        self.queryset=self.queryset.filter(adult_switch=input_ad)
        return self.queryset
    def filter_circle(self,input_circle):
        #input_circleはCircleModelのidのリストを入力する
        if(input_circle!=[]):
            query_empty=VoiceDataModel.objects.none()
            for x in input_circle:
                tmp=self.queryset.filter(circle=x)
                query_empty=query_empty|tmp
            self.queryset=query_empty
        return self.queryset
    def filter_cv(self,input_cv):
        if(input_cv!=[]):
            query_empty=VoiceDataModel.objects.none()
            for x in input_cv:
                tmp=self.queryset.filter(character_voice=x)
                query_empty=query_empty|tmp
            self.queryset=query_empty.distinct()
        return self.queryset
    def filter_scenario(self,input_scenario):
        if(input_scenario!=[]):
            query_empty=VoiceDataModel.objects.none()
            for x in input_scenario:
                tmp=self.queryset.filter(scenario_writers=x)
                query_empty=query_empty|tmp
            self.queryset=query_empty.distinct()
        return self.queryset
    def filter_genre(self,input_genre):
        if(input_genre!=[]):
            query_empty=VoiceDataModel.objects.none()
            for g in input_genre:
                one_genre_query=self.queryset.filter(genres=g)
                query_empty=query_empty|one_genre_query
            self.queryset=query_empty.distinct()
        return self.queryset
    def filter_keywords(self):
        if(self.dlsite_sch):
            for keyword in self.keywords_conv:
                self.queryset=self.queryset.filter(Q(maintext_conv__contains=keyword) | Q(description_conv__contains=keyword))
        else:
            for keyword in self.keywords_conv:
                self.queryset=self.queryset.filter(maintext_conv__contains=keyword)

        self.number_of_record=self.queryset.count()

    def filter_commond(self):
        for c in self.commond:
            cir_query=VoiceDataModel.objects.none()
            cv_query=VoiceDataModel.objects.none()
            sw_query=VoiceDataModel.objects.none()
            # サークル名でフィルタ
            cir_ids=self.get_circle_id_partial(c)
            if(cir_ids):
                q_objects = Q(circle=cir_ids[0])
                for id in cir_ids[1:]:
                    q_objects |= Q(circle=id)
                cir_query=self.queryset.filter(q_objects)

            # 声優名でフィルタ
            cv_ids=self.get_cv_id_partial(c)
            if(cv_ids):
                q_objects = Q(character_voice=cv_ids[0])
                for id in cv_ids[1:]:
                    q_objects |= Q(character_voice=id)
                cv_query=self.queryset.filter(q_objects)

            # シナリオライター名でフィルタ
            sw_ids=self.get_sw_id_partial(c)
            if(sw_ids):
                q_objects = Q(scenario_writers=sw_ids[0])
                for id in sw_ids[1:]:
                    q_objects |= Q(scenario_writers=id)
                sw_query=self.queryset.filter(q_objects)

            self.queryset=(cir_query | cv_query | sw_query).distinct()

    def exclude_keywords(self):
        if(self.dlsite_sch):
            for keyword in self.minus_keywords_conv:
                self.queryset=self.queryset.exclude(Q(maintext_conv__contains=keyword) | Q(description_conv__contains=keyword))
        else:
            for keyword in self.minus_keywords_conv:
                self.queryset=self.queryset.exclude(maintext_conv__contains=keyword)
        
    def exclude_commond(self):
        #input_commondはそのサークル、声優の名前でフィルターできる
        exclude_cmd=[]

        #サークルフィルター
        for c in self.minus_commond:
            tmp=self.get_circle_id(c)
            if(tmp):
                exclude_cmd.append(tmp)
        self.exclude_circle(exclude_cmd)
        exclude_cmd.clear()

        #声優フィルター
        for c in self.minus_commond:
            tmp=self.get_cv_id(c)
            if(tmp):
                exclude_cmd.append(tmp)
        self.exclude_cv(exclude_cmd)
        exclude_cmd.clear()

        #シナリオライターフィルター
        for c in self.minus_commond:
            tmp=self.get_sw_id(c)
            if(tmp):
                exclude_cmd.append(tmp)
        self.exclude_scenario(exclude_cmd)
        exclude_cmd.clear()
    def exclude_circle(self,input_circle):
        #input_circleはCircleModelのidのリストを入力する
        for x in input_circle:
            self.queryset=self.queryset.exclude(circle=x)
    def exclude_cv(self,input_cv):
        for x in input_cv:
            self.queryset=self.queryset.exclude(character_voice=x)
    def exclude_scenario(self,input_scenario):
        for x in input_scenario:
            self.queryset=self.queryset.exclude(scenario_writers=x)

    def set_keywords(self,joined_keywords):
        self.keywords=[]
        self.commond=[]
        self.minus_keywords=[]
        self.minus_commond=[]

        modify_ins=amadeus.ModifyText()

        joined_keywords=re.sub('\u3000',' ',joined_keywords) #全角スペースを半角スペースに変換
        joined_keywords=re.sub('＠','@',joined_keywords) #全角@を半角@に変換
        joined_keywords=re.sub('？','?',joined_keywords) #全角？を半角?に変換
        keywords=joined_keywords.split(' ')
        
        for i in keywords:
            if(i=='@all'):
                self.commond.append(i)
            elif(i in ['$','*','@',' ','ΦΦΦΦΦ','ΦΦΦΦ','ΦΦΦ','ΦΦ','Φ','',' ','　','\t']):
                pass
                # myprint(i+':NGword')
            elif(i[0]=='@'):
                self.commond.append(i[1:])
            elif(i[0]=='-'):
                if(i[0:2]=='-@'):
                    self.minus_commond.append(i[2:])
                else:
                    self.minus_keywords.append( re.escape(modify_ins.replace_fuseji(i[1:])))
            else:
                #伏せ字解除
                pattern=modify_ins.maru_pattern
                if(pattern.search(i)):
                    i=modify_ins.replace_fuseji(i)
                #メタ文字をエスケープする
                # self.keywords.append( re.escape(i) )

                # メタ文字をエスケープしない
                self.keywords.append(i)
        
        if('@all' in self.commond):
            self.keywords=[]
            (self.commond).remove('@all')

        self.keywords_conv=[ jaconv.kata2hira(i) for i in self.keywords ]
        self.minus_keywords_conv=[ jaconv.kata2hira(i) for i in self.minus_keywords ]
        # myprint(' '.join(self.keywords))
        # myprint(' '.join(self.commond))
        # myprint(' '.join(self.minus_commond))


        self.filter_commond()
        self.exclude_commond()
        self.exclude_keywords()
        self.filter_keywords()

    def search_keyword6(self,page=1):
            results_works = []
            results_works_info={}
            results_works_info_keywords_detail={}
            page=int(page)
            duration_end=page*50
            duration_start=duration_end-50
            if(duration_end>self.number_of_record):
                duration_end=self.number_of_record
                duration_start=duration_end-(self.number_of_record)%50
            
            selected_voicedata=self.queryset[duration_start:duration_end]
            for voicedata in selected_voicedata:
                display_range=voicedata.display_range
                keyword_count=0
                for (keyword_conv,keyword) in zip(self.keywords_conv,self.keywords):
                    match_text_fh,match_text_c,match_text_lh,chapter_name,hit_count=self.get_matchtext(
                        keyword_conv,
                        voicedata.maintext,
                        voicedata.maintext_conv,
                        voicedata.chapter_names,
                        display_range=display_range
                    )
                    font_color='red'
                    if(hit_count==0 and self.dlsite_sch):
                        match_text_fh,match_text_c,match_text_lh,chapter_name,hit_count=self.get_matchtext(
                            keyword_conv,
                            voicedata.description,
                            voicedata.description_conv,
                            '作品ページ',
                            display_range=display_range,
                        )
                        font_color='blue'
                    
                    results_works_info_keywords_detail['hit_count']=hit_count
                    results_works_info_keywords_detail['color']=font_color

                    if(font_color=='blue'):
                        results_works_info_keywords_detail['status']=chapter_name+' より'
                    else:
                        if(voicedata.sample_switch):
                            results_works_info_keywords_detail['status']='サンプル {0} より'.format(chapter_name)
                        else:
                            results_works_info_keywords_detail['status']='台本 {0} より'.format(chapter_name)

                    results_works_info_keywords_detail['keyword']=match_text_c
                    results_works_info_keywords_detail['text_fh']=match_text_fh
                    results_works_info_keywords_detail['text_lh']=match_text_lh
                    results_works_info_keywords_detail['chapter_name']=chapter_name

                    results_works_info['keyword'+str(keyword_count)]=json.dumps(results_works_info_keywords_detail)
                    keyword_count+=1

                results_works_info['id']=voicedata.id
                results_works_info['public_record_id']=voicedata.public_record_id
                results_works_info['title']=voicedata.name
                results_works_info['url']=voicedata.url
                results_works_info['url_img']=voicedata.url_img
                results_works_info['circle']=voicedata.circle.circle
                cv='/'.join([x.character_voice for x in voicedata.character_voice.all()])
                results_works_info['cv1']=cv
                results_works_info['scenario']='/'.join([x.scenario_writer for x in voicedata.scenario_writers.all()])
                results_works_info['work_id']=voicedata.work_id
                results_works.append(copy.copy(results_works_info))

            self.results_works=results_works

    def sort_queryset(self,input_order):

        if(input_order):
            menucodes=["release_date_ascending","release_date_descending","add_date_ascending","add_date_descending"]
            menucode=menucodes[int(input_order)-1]
        else:
            menucode="add_date_descending"

        if(menucode=='release_date_ascending'):
            self.queryset=self.queryset.order_by('release_date')
        elif(menucode=='release_date_descending'):
            self.queryset=self.queryset.order_by('release_date').reverse()
        elif(menucode=='add_date_ascending'):
            self.queryset=self.queryset.order_by('add_date')
        elif(menucode=='add_date_descending'):
            self.queryset=self.queryset.order_by('add_date').reverse()
        else:
            self.queryset=self.queryset.order_by('add_date').reverse()

    def adjust_letter_divide(self,text,start,end,display_range):
        start_back=start-display_range
        if(start_back<0):
            start_back=0
        end_front=end+display_range
        if(end_front>len(text)):
            end_front=len(text)
        text_fh=text[start_back:start]
        text_lf=text[end:end_front]
        text_c=text[start:end]
        return text_fh,text_c,text_lf

    def get_matchtext(self, keyword_conv, text, text_conv, chapter_names_str,display_range=100):
        # match_text_fh,match_text_c,match_text_lh,chapter_name,hit_count
        # pattern = re.compile(keyword_conv, re.IGNORECASE)
        pattern=re.escape(keyword_conv)

        if (chapter_names_str):
            chapter_names = chapter_names_str.split('ΦΦΦΦΦ')
            chapter_texts = text.split('ΦΦΦΦΦ')
            chapter_texts_conv = text_conv.split('ΦΦΦΦΦ')

            if len(chapter_names) != len(chapter_texts):
                chapter_names = ['サンプルAI書き起こし' for _ in chapter_texts]

            num_chap = len(chapter_names)
            selector_list = random.sample(range(num_chap), k=num_chap)

            for selector in selector_list:
                matches = list(re.finditer(pattern,chapter_texts_conv[selector]))
                chapter_text=chapter_texts[selector]
                chapter_name=chapter_names[selector]
                if matches:
                    break
            
            if(matches):
                match=random.choice(matches)
                match_text_fh,match_text_c,match_text_lh=self.adjust_letter_divide(chapter_text,match.start(),match.end(),display_range)

                return match_text_fh,match_text_c,match_text_lh,chapter_name,len(matches)


            return '','','','',0

        else:
            return '','','','',0

    def get_circle_id(self,name):
        try:
            return CircleModel.objects.get(alias=name).id
        except ObjectDoesNotExist:
            return False
    def get_cv_id(self,name):
        try:
            return CharacterVoiceModel.objects.get(alias=name).id
        except ObjectDoesNotExist:
            return False
    def get_sw_id(self,name):
        try:
            return ScenarioWriterModel.objects.get(alias=name).id
        except ObjectDoesNotExist:
            return False
    def get_circle_id_partial(self,name):
        # nameが完全一致するばあいは1つだけ返す、部分一致の場合は複数返す
        try:
            return [CircleModel.objects.get(circle=name).id]
        except ObjectDoesNotExist:
            query=CircleModel.objects.filter(circle__icontains=name)
            return [q.id for q in query]
    def get_cv_id_partial(self,name):
        # nameが完全一致するばあいは1つだけ返す、部分一致の場合は複数返す
        try:
            return [CharacterVoiceModel.objects.get(character_voice=name).id]
        except ObjectDoesNotExist:
            query=CharacterVoiceModel.objects.filter(character_voice__icontains=name)
            return [q.id for q in query]
    def get_sw_id_partial(self,name):
        # nameが完全一致するばあいは1つだけ返す、部分一致の場合は複数返す
        try:
            return [ScenarioWriterModel.objects.get(scenario_writer=name).id]
        except ObjectDoesNotExist:
            query=ScenarioWriterModel.objects.filter(scenario_writer__icontains=name)
            return [q.id for q in query]

    def search_from_memo(self,memo_Base64):
        # そのうち廃止する
        def decode_string(encoded_str):
            # Base64データをバイトデータにデコードする
            byte_data = base64.b64decode(encoded_str)
            # バイトデータをUTF-8文字列に変換する
            return byte_data.decode('utf-8')
        
        memo=decode_string(memo_Base64)
        public_record_id,chapter_num,start_pos,end_pos,isDlsite=memo.split('/')
        chapter_num=int(chapter_num)
        start_pos=int(start_pos)
        end_pos=int(end_pos)

        results_works_info={}
        results_works_info_keywords_detail={}
        queryset=VoiceDataModel.objects.all()
        queryset=queryset.filter(public_record_id=public_record_id)

        for voicedata in queryset:
            id=voicedata.id
            maintext=(voicedata.maintext_old).split('ΦΦΦΦΦ')[chapter_num]
            chapter_names=voicedata.chapter_names
            if(chapter_names and chapter_num<len(chapter_names)):
                chapter_name=(voicedata.chapter_names).split('ΦΦΦΦΦ')[chapter_num]
            else:
                chapter_name=''
            display_range=voicedata.display_range
            text_fh,text_c,text_lh=self.adjust_letter_divide(maintext,start_pos,end_pos,display_range)

            results_works_info_keywords_detail['keyword']=text_c
            results_works_info_keywords_detail['text_fh']=text_fh
            results_works_info_keywords_detail['text_lh']=text_lh
            results_works_info_keywords_detail['start_pos']=start_pos
            results_works_info_keywords_detail['end_pos']=end_pos
            results_works_info_keywords_detail['chapter_num']=chapter_num
            results_works_info_keywords_detail['status']='サンプル {0} より'.format(chapter_name)
            results_works_info_keywords_detail['hit_count']=1
            results_works_info_keywords_detail['color']='red'

            results_works_info['id']=voicedata.id
            results_works_info['public_record_id']=voicedata.public_record_id
            results_works_info['url_edit']='https://woxram.com/django/xyz/admin/app1/voicedatamodel/'+str(voicedata.id)+'/change/'
            results_works_info['title']=voicedata.name
            results_works_info['url']=voicedata.url
            results_works_info['url_img']=voicedata.url_img
            results_works_info['circle']=voicedata.circle.circle
            cv='/'.join([x.character_voice for x in voicedata.character_voice.all()])
            results_works_info['cv1']=cv
            results_works_info['scenario']='/'.join([x.scenario_writer for x in voicedata.scenario_writers.all()])
            results_works_info['work_id']=voicedata.work_id
            results_works_info['keyword0']=json.dumps(results_works_info_keywords_detail)

        queryset=MemoData.objects.all()
        if(not( queryset.filter(public_id=str(memo_Base64)).exists() )):
            obj=MemoData(
                public_id=(memo_Base64),
                public_record_id=public_record_id,
                info="red",
                chapter_name=chapter_name,
                text='ΦΦΦΦΦ'.join([text_fh,text_c,text_lh])
            )
            obj.save()

        return [results_works_info]

    def search_from_memo_database(self,public_id):
        memo=MemoData.objects.get(public_id=public_id)
        voicedata=VoiceDataModel.objects.get(public_record_id=memo.public_record_id)
        text_fh,text_c,text_lh=(memo.text).split('ΦΦΦΦΦ')
        

        results_works_info={}
        results_works_info_keywords_detail={}
        results_works_info_keywords_detail['keyword']=text_c
        results_works_info_keywords_detail['text_fh']=text_fh
        results_works_info_keywords_detail['text_lh']=text_lh
        results_works_info_keywords_detail['status']='サンプル {0} より'.format(memo.chapter_name)
        results_works_info_keywords_detail['hit_count']=1
        results_works_info_keywords_detail['color']=memo.info

        results_works_info['id']=voicedata.id
        results_works_info['public_record_id']=voicedata.public_record_id
        results_works_info['url_edit']='https://woxram.com/django/xyz/admin/app1/voicedatamodel/'+str(voicedata.id)+'/change/'
        results_works_info['title']=voicedata.name
        results_works_info['url']=voicedata.url
        results_works_info['url_img']=voicedata.url_img
        results_works_info['circle']=voicedata.circle.circle
        cv='/'.join([x.character_voice for x in voicedata.character_voice.all()])
        results_works_info['cv1']=cv
        results_works_info['scenario']='/'.join([x.scenario_writer for x in voicedata.scenario_writers.all()])
        results_works_info['work_id']=voicedata.work_id
        results_works_info['keyword0']=json.dumps(results_works_info_keywords_detail)

        return [results_works_info]

class SearchInfo:
    def __init__(self,request_post):
        self.keywords,self.keywords_conv=self.getKeywords(request_post)
        self.joined_keywords=request_post.get('keyword')
        self.character_voice_checkbox=self.getCvCheckbox(request_post)
        self.circle_checkbox=self.getCircleCheckbox(request_post)
        self.scenario_checkbox=self.getScenarioCheckbox(request_post)
        self.genres_checkbox=self.getGenreCheckbox(request_post)

        self.sample_switch=self.get_sample_switch(request_post)
        self.order_input=request_post.get('order')
        self.dlsite_sch=self.getDlsiteSch(request_post)

    def getKeywords(self,request_post):
        keyword_input=request_post.get('keyword')

        keyword_input=re.sub('\u3000',' ',keyword_input) #全角スペースを半角スペースに変換
        keywords=keyword_input.split(' ')

        keyword_input=jaconv.kata2hira(keyword_input)
        keywords_conv=keyword_input.split(' ')

        return keywords,keywords_conv
    def getCvCheckbox(self,request_post):
        #声優のチェックボックスを読み取り
        character_voice_checkbox=request_post.getlist('character_voice_checkbox_az')
        character_voice_checkbox.extend(request_post.getlist('character_voice_checkbox_a'))
        character_voice_checkbox.extend(request_post.getlist('character_voice_checkbox_ka'))
        character_voice_checkbox.extend(request_post.getlist('character_voice_checkbox_sa'))
        character_voice_checkbox.extend(request_post.getlist('character_voice_checkbox_ta'))
        character_voice_checkbox.extend(request_post.getlist('character_voice_checkbox_na'))
        character_voice_checkbox.extend(request_post.getlist('character_voice_checkbox_ha'))
        character_voice_checkbox.extend(request_post.getlist('character_voice_checkbox_ma'))
        character_voice_checkbox.extend(request_post.getlist('character_voice_checkbox_ya'))
        character_voice_checkbox.extend(request_post.getlist('character_voice_checkbox_ra'))
        character_voice_checkbox.extend(request_post.getlist('character_voice_checkbox_wa'))
        return character_voice_checkbox
    def getCircleCheckbox(self,request_post):
        #サークルのチェックボックスを読み取り
        circle_checkbox=request_post.getlist('circle_checkbox_az')
        circle_checkbox.extend(request_post.getlist('circle_checkbox_a'))
        circle_checkbox.extend(request_post.getlist('circle_checkbox_ka'))
        circle_checkbox.extend(request_post.getlist('circle_checkbox_sa'))
        circle_checkbox.extend(request_post.getlist('circle_checkbox_ta'))
        circle_checkbox.extend(request_post.getlist('circle_checkbox_na'))
        circle_checkbox.extend(request_post.getlist('circle_checkbox_ha'))
        circle_checkbox.extend(request_post.getlist('circle_checkbox_ma'))
        circle_checkbox.extend(request_post.getlist('circle_checkbox_ya'))
        circle_checkbox.extend(request_post.getlist('circle_checkbox_ra'))
        circle_checkbox.extend(request_post.getlist('circle_checkbox_wa'))
        return circle_checkbox
    def getScenarioCheckbox(self,request_post):
        #シナリオのチェックボックスを読み取り
        scenario_checkbox=request_post.getlist('scenario_checkbox_az')
        scenario_checkbox.extend(request_post.getlist('scenario_checkbox_a'))
        scenario_checkbox.extend(request_post.getlist('scenario_checkbox_ka'))
        scenario_checkbox.extend(request_post.getlist('scenario_checkbox_sa'))
        scenario_checkbox.extend(request_post.getlist('scenario_checkbox_ta'))
        scenario_checkbox.extend(request_post.getlist('scenario_checkbox_na'))
        scenario_checkbox.extend(request_post.getlist('scenario_checkbox_ha'))
        scenario_checkbox.extend(request_post.getlist('scenario_checkbox_ma'))
        scenario_checkbox.extend(request_post.getlist('scenario_checkbox_ya'))
        scenario_checkbox.extend(request_post.getlist('scenario_checkbox_ra'))
        scenario_checkbox.extend(request_post.getlist('scenario_checkbox_wa'))
        return scenario_checkbox
    def getGenreCheckbox(self,request_post):
        #ジャンルのチェックボックスを読み取り
        genres_checkbox=request_post.getlist('genres_checkbox_az')
        genres_checkbox.extend(request_post.getlist('genres_checkbox_a'))
        genres_checkbox.extend(request_post.getlist('genres_checkbox_ka'))
        genres_checkbox.extend(request_post.getlist('genres_checkbox_sa'))
        genres_checkbox.extend(request_post.getlist('genres_checkbox_ta'))
        genres_checkbox.extend(request_post.getlist('genres_checkbox_na'))
        genres_checkbox.extend(request_post.getlist('genres_checkbox_ha'))
        genres_checkbox.extend(request_post.getlist('genres_checkbox_ma'))
        genres_checkbox.extend(request_post.getlist('genres_checkbox_ya'))
        genres_checkbox.extend(request_post.getlist('genres_checkbox_ra'))
        genres_checkbox.extend(request_post.getlist('genres_checkbox_wa'))
        return genres_checkbox
    def getDlsiteSch(self,request_post):
        dlsite_sch=request_post.get('dlsite')
        if(dlsite_sch=='on'):
            dlsite_sch=True
        else:
            dlsite_sch=False
        return dlsite_sch
    def get_sample_switch(self,request_post):
        sample=request_post.get('sample')
        if(sample=='on'):
            sample=True
        else:
            sample=False
        return sample


from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from app1.models import CircleModel, CharacterVoiceModel, ScenarioWriterModel, VoiceDataModel
from api1.models import SearchExample
from account.models import MemoData

# Create your views here.
class getCircle (APIView):
    def get(self,request):
        id_input=request.GET.get("id")
        records=CircleModel.objects.filter(id=id_input)
        if(records.exists()):
            for record in records:
                return Response({
                    "name":record.circle,
                    "id":record.circle_id,
                    "url":record.url_circle,
                })
        else:
            return Response(False)

class getCV (APIView):
    def get(self,request):
        id_input=request.GET.get("id")
        records=CharacterVoiceModel.objects.filter(id=id_input)
        if(records.exists()):
            for record in records:
                return Response({
                    "name":record.character_voice,
                })
        else:
            return Response(False)

class getScenariowriter (APIView):
    def get(self,request):
        id_input=request.GET.get("id")
        records=ScenarioWriterModel.objects.filter(id=id_input)
        if(records.exists()):
            for record in records:
                return Response({
                    "name":record.scenario_writer,
                })
        else:
            return Response(False)

class getVoicedata(APIView):
    def get(self,request):
        id_input=request.GET.get("id")
        records=VoiceDataModel.objects.filter(id=id_input)
        if(records.exists()):
            for record in records:
                return Response({
                    "public_record_id":record.public_record_id,
                    "name":record.name,
                    "work_id":record.work_id,
                    "circle":record.circle.circle,
                    "circle_id":record.circle.circle_id,
                    "release_date":record.release_date,
                    "add_date":record.add_date,
                    "character_voice":[x.character_voice for x in record.character_voice.all()],
                    "url":record.url,
                    "url_img":record.url_img,
                    "commerce_switch":record.commerce_switch,
                    "public_switch":record.public_switch,
                    "public_delete":record.public_delete,
                    "sample_switch":record.sample_switch,
                    "adult_switch":record.adult_switch,
                    "display_range":record.display_range,
                    "scenario_writers":[x.scenario_writer for x in record.scenario_writers.all()],
                    "description":record.description,
                    "description_original":record.description_original,
                    "description_conv":record.description_conv,
                    "chapter_names":record.chapter_names,
                    "maintext_original":record.maintext_original,
                    "maintext":record.maintext,
                    "maintext_conv":record.maintext_conv,
                    "maintext_old":record.maintext_old,
                    "text_version":record.text_version,
                })
        else:
            return Response(False)


class getSearchExample (APIView):
    def get(self,request):
        id_input=request.GET.get("id")
        records=SearchExample.objects.filter(id=id_input)
        if(records.exists()):
            for record in records:
                return Response({
                    "url":record.url,
                    "keyword":record.keyword,
                })
        else:
            return Response(False)

class getMemodata (APIView):
    def get(self,request):
        id_input=request.GET.get("id")
        records=MemoData.objects.filter(id=id_input)
        if(records.exists()):
            for record in records:
                return Response({
                    "public_id":record.public_id,
                    "public_record_id":record.public_record_id,
                    "info":record.info,
                    "chapter_name":record.chapter_name,
                    "text":record.text,
                })
        else:
            return Response(False)
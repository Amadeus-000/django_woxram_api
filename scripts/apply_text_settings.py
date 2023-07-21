from app1.models import VoiceDataModel
from app1 import amadeus
import jaconv,re

#Amadeusに登録されているTextStandardに基づいてmaintext_originalをModifyingする
#TSWでwhisper書き起こしのみ変更する。
def run():
    queryset=VoiceDataModel.objects.all()
    queryset=queryset.filter(maintext_conv__contains='\r\n')
    # queryset=queryset.filter(id=15492)
    for q in queryset:
        print(q.id)
        print(q.work_text_state.code)
        print(q.name)
        mt_ins=amadeus.ModifyText(q.maintext_original, q.work_text_state.code)
        q.maintext=mt_ins.text
        q.maintext_conv=mt_ins.text_conv
        q.save()
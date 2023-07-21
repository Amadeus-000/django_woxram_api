from app1.models import VoiceDataModel
from app1 import amadeus
from app1.views import AddWork
import jaconv,re

#WorkInfoをDLsiteから直接データを持って来て修正する
def run():
    queryset=VoiceDataModel.objects.all()
    record=queryset.get(id=16431)
    print(record.id)
    obj=amadeus.WorkInfo(record.url)
    # record.name=obj.title
    record.scenario_writers.clear()
    for sw in obj.author:
        addwork_ins=AddWork(obj)
        record.scenario_writers.add(addwork_ins.check_create_sw(sw))
        record.save()
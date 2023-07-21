from app1.models import CircleModel,CharacterVoiceModel, ScenarioWriterModel

#サークル、声優、シナリオの名前で重複しているもの訂正する。
#サークル＞声優、シナリオの順序で名前分けしている。
def run():
    queryset=CircleModel.objects.all()
    for q in queryset:
        q.alias=(q.circle).replace(' ', '_')
        q.save()
    queryset=CharacterVoiceModel.objects.all()
    for q in queryset:
        q.alias=(q.character_voice).replace(' ', '_')
        q.save()
    queryset=ScenarioWriterModel.objects.all()
    for q in queryset:
        q.alias=(q.scenario_writer).replace(' ', '_')
        q.save()
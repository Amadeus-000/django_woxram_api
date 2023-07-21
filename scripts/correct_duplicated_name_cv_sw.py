from app1.models import CircleModel,CharacterVoiceModel, ScenarioWriterModel

#声優、シナリオの名前で重複しているもの訂正する。
#声優>シナリオの順序で名前分けしている。
def run():
    cv=[]
    sw=[]
    queryset=CharacterVoiceModel.objects.all()
    for q in queryset:
        cv.append(q.character_voice)
        q.alias=(q.character_voice).replace(' ', '_')
        q.save()
    queryset=ScenarioWriterModel.objects.all()
    for q in queryset:
        sw.append(q.scenario_writer)
        q.alias=(q.scenario_writer).replace(' ', '_')
        q.save()

    cv=set(cv)
    sw=set(sw)


    cv_and_sw=list(cv & sw)


    #声優　シナリオ　の重複
    print('声優　シナリオ　の重複 @@@@@@@@@@@@')
    # queryset_cv=CharacterVoiceModel.objects.all()
    queryset_sw=ScenarioWriterModel.objects.all()
    for x in cv_and_sw:
        # record=queryset_cv.get(character_voice=x)
        # record.alias=(record.character_voice).replace(' ', '_')+'(声優)'
        # print(record.alias)
        # record.save()

        record=queryset_sw.get(scenario_writer=x)
        record.alias=(record.scenario_writer).replace(' ', '_')+'(シナリオ)'
        print(record.alias)
        record.save()
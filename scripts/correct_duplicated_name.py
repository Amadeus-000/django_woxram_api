from app1.models import CircleModel,CharacterVoiceModel, ScenarioWriterModel

#サークル、声優、シナリオの名前で重複しているもの訂正する。
#サークル＞声優、シナリオの順序で名前分けしている。
def run():
    circle=[]
    cv=[]
    sw=[]
    queryset=CircleModel.objects.all()
    for q in queryset:
        circle.append(q.circle)
        q.alias=(q.circle).replace(' ', '_')
        q.save()
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

    circle=set(circle)
    cv=set(cv)
    sw=set(sw)

    cir_and_cv=list( (circle & cv) - (circle & cv & sw) )
    cir_and_sw=list( (circle & sw) - (circle & cv & sw) )
    cv_and_sw=list( (cv & sw) - (circle & cv & sw) )
    cir_and_cv_and_sw=list(circle & cv & sw)

    #サークル　声優　の重複
    print('サークル　声優　の重複 @@@@@@@@@@@@')
    queryset=CharacterVoiceModel.objects.all()
    for x in cir_and_cv:
        record=queryset.get(character_voice=x)
        record.alias=(record.character_voice).replace(' ', '_')+'(声優)'
        print(record.alias)
        record.save()
    
    #サークル　シナリオ　の重複
    print('サークル　シナリオ　の重複 @@@@@@@@@@@@')
    queryset=ScenarioWriterModel.objects.all()
    for x in cir_and_sw:
        record=queryset.get(scenario_writer=x)
        record.alias=(record.scenario_writer).replace(' ', '_')+'(シナリオ)'
        print(record.alias)
        record.save()

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

    #サークル　声優　シナリオ　の重複
    print('サークル　声優　シナリオ　の重複 @@@@@@@@@@@@')
    queryset_cv=CharacterVoiceModel.objects.all()
    queryset_sw=ScenarioWriterModel.objects.all()
    for x in cir_and_cv_and_sw:
        record=queryset_cv.get(character_voice=x)
        record.alias=(record.character_voice).replace(' ', '_')+'(声優)'
        print(record.alias)
        record.save()

        record=queryset_sw.get(scenario_writer=x)
        record.alias=(record.scenario_writer).replace(' ', '_')+'(シナリオ)'
        print(record.alias)
        record.save()
        

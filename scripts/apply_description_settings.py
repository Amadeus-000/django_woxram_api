from app1.models import VoiceDataModel
from app1 import amadeus
import jaconv,re,os,sys

#Amadeusに登録されているTextStandardに基づいてmaintext_originalをModifyingする
#TSWでwhisper書き起こしのみ変更する。
def run():
    # モジュールが含まれるディレクトリの絶対パスを取得
    module_dir = os.path.abspath(os.path.dirname("/home/iroha/Amadeus/amadeus.py"))
    print(module_dir)
    # 絶対パスをシステムパスに追加
    sys.path.insert(0, module_dir)
    # モジュールをインポート
    import amadeus

    amadeus.VersionInfo()

    queryset=VoiceDataModel.objects.all()
    # queryset=queryset.filter(id=26903)
    for q in queryset[20000:]:
        print(q.id)
        # print('Modifying work. id={0}'.format(q.id))

        cv_str='/'.join([str(x) for x in q.character_voice.all()])
        cir_str=q.circle.circle
        sw_str='/'.join([str(x) for x in q.scenario_writers.all()])
        title=q.name

        descripton_info='{0}\n{1}\n{2}\n{3}'.format(title,cir_str,cv_str,sw_str)
        description_original=q.description_original
        description=descripton_info + '\n\n' + description_original
        modify_text=amadeus.ModifyText(description,text_type='description')
        description=modify_text.text
        description_conv=modify_text.text_conv

        q.description=description
        q.description_conv=description_conv
        q.save()

import sys
import os
import time

from app1.models import VoiceDataModel

def run():
    # モジュールが含まれるディレクトリの絶対パスを取得
    module_dir = os.path.abspath(os.path.dirname("/home/iroha/Amadeus/amadeus.py"))
    # print(module_dir)
    # 絶対パスをシステムパスに追加
    sys.path.insert(0, module_dir)
    # モジュールをインポート
    import amadeus

    records=VoiceDataModel.objects.all()
    records=records.filter(sample_switch=True).order_by('id')
    # records=records.filter(id="24880")
    records=records.filter(id__range=(6566,6570))

    for record in records:
        print(record.id)
        ins=amadeus.ModifyText(record.maintext,text_type='update')
        record.maintext_old=record.maintext
        record.maintext=ins.text
        record.maintext_conv=ins.text_conv
        record.save()
        time.sleep(10)
    
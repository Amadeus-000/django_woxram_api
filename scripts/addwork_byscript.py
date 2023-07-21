from app1.models import VoiceDataModel
from app1.views import AddWork
# from app1 import amadeus
import jaconv,re,os,sys

def run():
    # モジュールが含まれるディレクトリの絶対パスを取得
    module_dir = os.path.abspath(os.path.dirname("/home/iroha/Amadeus/amadeus.py"))
    print(module_dir)
    # 絶対パスをシステムパスに追加
    sys.path.insert(0, module_dir)
    # モジュールをインポート
    import amadeus

    # circles=['20230313']
    circles=sorted(os.listdir('/home/iroha/outputdata/outputdata'))
    circles.remove('log.txt')
    
    print(circles)
    err_message=[]

    for circle in circles:
        circlepath='/home/iroha/outputdata/outputdata/{0}/workinfo'.format(circle)
        works=sorted(os.listdir(circlepath))
        print(works)
        for work in works:
            workpath='{0}/{1}'.format(circlepath,work)
            print(workpath)
            with open(workpath + '/info.txt','r',encoding='utf-8')as f:
                infotxt=f.read()
                # print(infotxt)
            with open(workpath + '/filename_str.txt','r',encoding='utf-8')as f:
                filename_str=f.read()
                # print(filename_str)
            with open(workpath + '/output.txt','r',encoding='utf-8')as f:
                maintext=f.read()
                # print(maintext)
            workinfo_ins=amadeus.WorkInfo()
            workinfo_ins.initialize_by_txt(infotxt)

            addwork_ins=AddWork(
                workinfo_ins,
                maintext_original=maintext,
                commerce_switch=True,
                public_switch=True,
                sample_switch=True,
                display_range=100,
                chapter_names_str=filename_str,
                create_user='',
                work_text_state_code='TSW_v3',
            )

            koushin=True
            if(koushin):
                message=addwork_ins.update_maintext()
                print(message)
            else:
                message=addwork_ins.make_record()
                print(message)

            if(message[-1]=='4'):
                err_message.append
    print(err_message)


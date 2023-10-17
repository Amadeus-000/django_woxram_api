from app1.models import VoiceDataModel

# chapter_nameの数とmaintextの数が同じかどうかチェックする
# chapter_nameが''とNoneのときは除く
def run():
    queryset=VoiceDataModel.objects.all()
    for q in queryset:
        if(q.chapter_names=='' or q.chapter_names==None):
            if(q.maintext):
                print('empty {0}'.format(q.id))
        else:
            chapter_names=q.chapter_names
            maintext=q.maintext
            chapter_num=len((chapter_names).split('ΦΦΦΦΦ'))
            maintext_num=len((maintext).split('ΦΦΦΦΦ'))
            if(chapter_num!=maintext_num):
                print('mismatch!!!!!')
                print('id={0}\nwork_id={1}'.format(q.id,q.work_id))
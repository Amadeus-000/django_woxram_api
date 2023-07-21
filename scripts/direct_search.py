from app1.models import VoiceDataModel
import re
import time

def run():
    X=r'[\n、。… \?]*'
    keyword='おちんちん\+種付け'
    print(list(keyword))
    start=time.time()
    keyword_x=''
    for c in keyword[:-2]:
        keyword_x=keyword_x+re.escape(c)+X
    keyword_x=keyword_x+keyword[-1]
    end=time.time()
    print(end-start)
    # keyword=r'ですか\?'

    start=time.time()
    keyword_x=X.join(keyword)
    end=time.time()
    print(end-start)
    print(keyword_x)

    # print(queryset.get(id=1000))
    
    # queryset=VoiceDataModel.objects.all()
    # queryset_c=queryset.filter(description_conv__contains=keyword)
    # queryset_r=queryset.filter(maintext_conv__regex=keyword_x)
    
    # print(queryset_c.count())
    # print(queryset_r.count())

    # for i,j in zip(queryset_c,queryset_r):
    #     if(i.id==j.id):
    #         print('same!')
    #     else:
    #         print('{0} is Not same!'.format(i.id))


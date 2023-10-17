from rest_framework.views import APIView
from rest_framework.response import Response

from django.middleware.csrf import get_token
from django.http import JsonResponse

from app1.models import VoiceDataModel
from .models import MemoData

import string,random,jaconv,re

import amadeus
from utility.utils import AddWork


from django.utils.decorators import method_decorator
# キャッシュを無効
from django.views.decorators.cache import never_cache
# CSRFトークンを無効
from django.views.decorators.csrf import csrf_exempt

# @method_decorator(csrf_exempt, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class GetMemoPublicId(APIView):
    # def get(self,request):
    #     if(request.GET.get("public_record_id",False)):
    #         public_record_id=request.GET.get("public_record_id","")
    #         chapter_num=int(request.GET.get("chapter_num",0))
    #         start_pos=int(request.GET.get("start_pos",0))
    #         end_pos=int(request.GET.get("end_pos",0))
    #         info=request.GET.get("color","red")

    #         voicedata=VoiceDataModel.objects.get(public_record_id=public_record_id)

    #         maintext=(voicedata.maintext_old).split('ΦΦΦΦΦ')[chapter_num]
    #         chapter_name=(voicedata.chapter_names).split('ΦΦΦΦΦ')[chapter_num]
    #         text_fh,keyword,text_lh=self.adjust_letter_divide(maintext,start_pos,end_pos,voicedata.display_range)
    #         memo_text='ΦΦΦΦΦ'.join([text_fh,keyword,text_lh])

    #         memodata=MemoData.objects.all()
    #         memodata=memodata.filter(public_record_id=public_record_id).filter(info=info).filter(chapter_name=chapter_name).filter(text=memo_text)
    #         if(memodata.exists()):
    #             for i in memodata:
    #                 return Response(i.public_id)
    #         else:
    #             obj=MemoData(
    #                 public_id='memo'+self.generate_random_string(32),
    #                 public_record_id=public_record_id,
    #                 info=info,
    #                 chapter_name=chapter_name,
    #                 text=memo_text,
    #             )
    #             obj.save()

    #         return Response(obj.public_id)
    #     else:
    #         return Response(0)

    def get(self,request):
        if(request.GET.get("public_record_id",False)):

            public_record_id=request.GET.get("public_record_id")
            text_fh=request.GET.get("text_fh")
            keyword=request.GET.get("keyword")
            text_lh=request.GET.get("text_lh")
            chapter_name=request.GET.get("chapter_name")
            info=request.GET.get("color")

            memo_text='ΦΦΦΦΦ'.join([text_fh,keyword,text_lh])

            memodata=MemoData.objects.all()
            memodata=memodata.filter(public_record_id=public_record_id).filter(info=info).filter(chapter_name=chapter_name).filter(text=memo_text)
            if(memodata.exists()):
                for i in memodata:
                    return Response(i.public_id)
            else:
                obj=MemoData(
                    public_id='memo'+self.generate_random_string(32),
                    public_record_id=public_record_id,
                    info=info,
                    chapter_name=chapter_name,
                    text=memo_text,
                )
                obj.save()

            return Response(obj.public_id)
        else:
            return Response(0)

    def post(self,request):
        public_record_id=request.data.get("public_record_id")
        text_fh=request.data.get("text_fh")
        keyword=request.data.get("keyword")
        text_lh=request.data.get("text_lh")
        chapter_name=request.data.get("chapter_name")
        info=request.data.get("color")

        memo_text='ΦΦΦΦΦ'.join([text_fh,keyword,text_lh])

        memodata=MemoData.objects.all()
        memodata=memodata.filter(public_record_id=public_record_id).filter(info=info).filter(chapter_name=chapter_name).filter(text=memo_text)
        if(memodata.exists()):
            for i in memodata:
                return Response(i.public_id)
        else:
            obj=MemoData(
                public_id='memo'+self.generate_random_string(32),
                public_record_id=public_record_id,
                info=info,
                chapter_name=chapter_name,
                text=memo_text,
            )
            obj.save()

        return Response(obj.public_id)

    # @method_decorator(csrf_exempt)
    # def dispatch(self, *args, **kwargs):
    #     return super(GetMemoPublicId, self).dispatch(*args, **kwargs)

    def adjust_letter_divide(self,text,start,end,display_range):
        start_back=start-display_range
        if(start_back<0):
            start_back=0
        end_front=end+display_range
        if(end_front>len(text)):
            end_front=len(text)
        text_fh=text[start_back:start]
        text_lf=text[end:end_front]
        text_c=text[start:end]
        return text_fh,text_c,text_lf
    def generate_random_string(self,length):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join(random.choice(letters_and_digits) for _ in range(length))
        return result_str
    

class AddworkForUser(APIView):
    def get(self,request):
        maintext=request.GET.get('maintext')
        with open('output.txt','w',encoding='utf-8') as f:
            f.write(str(maintext))

        return Response(maintext)

    def post(self,request):
        maintexts_original=request.data["maintexts"]
        chapter_names=request.data["chapter_names"]
        uid=request.data["uid"]
        url=request.data["url"]

        with open("tmp/output.txt","w",encoding='utf-8') as f:
            f.write(str(maintexts_original))

        workinfo=amadeus.WorkInfo(url)

        maintexts=[]
        maintexts_conv=[]
        for m in maintexts_original:
            modify=amadeus.ModifyText(m)
            maintexts.append(modify.text)
            maintexts_conv.append(modify.text_conv)

        addwork=AddWork(
            workinfo,
            commerce_switch=True,
            sample_switch=False,
            public_switch=True,
            display_range=100,
            maintexts_original=maintexts_original,
            maintexts=maintexts,
            maintexts_conv=maintexts_conv,
            chapter_names=chapter_names,
            text_version="script,",
            uid=uid,
        )
        addwork.make_records()

        return Response("Success!")
    


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

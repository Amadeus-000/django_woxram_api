from app1.models import SearchLog
def run():
    queryset=SearchLog.objects.all()
    for i in queryset:
        print(i.adddate)
from django.db import models

class MemoData(models.Model):
    public_id=models.CharField(max_length=64,default="")
    public_record_id=models.CharField(max_length=32,default="")
    info=models.CharField(max_length=32,default="")
    chapter_name=models.CharField(max_length=512,default="")
    text=models.TextField(null=True,blank=True)
    uid=models.CharField(max_length=64,default="",null=True,blank=True)
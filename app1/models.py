from django.db import models
from datetime import datetime
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

# Create your models here.

def create_public_record_id():
    #この関数を挟んで関数を括弧なしで呼び出さないと、固定の乱数がdefaultになってしまう
    return get_random_string(25)

class CharacterVoiceModel(models.Model):
    character_voice=models.CharField(max_length=256)
    yomigana=models.CharField(max_length=256,blank=True,null=True)
    cv_id=models.CharField(max_length=32,blank=True,null=True)
    def __str__(self):
        return self.character_voice
    class Meta:
        #verbose_name = "VoiceActor lists(VoiceactorModel)"
        verbose_name_plural = "character voice lists"

class CircleModel(models.Model):
    circle=models.CharField(max_length=256)
    yomigana=models.CharField(max_length=256,blank=True,null=True)
    circle_id=models.CharField(max_length=16,blank=True,null=True)
    url_circle=models.CharField(max_length=127,blank=True,null=True)
    publication_state=models.CharField(max_length=16,blank=True,null=True)
    approval_state=models.CharField(max_length=16,blank=True,null=True)
    supplement=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.circle
    class Meta:
        verbose_name_plural="Circle lists"

class ScenarioWriterModel(models.Model):
    scenario_writer=models.CharField(max_length=256,blank=True,null=True)
    yomigana=models.CharField(max_length=256,blank=True,null=True)
    sw_id=models.CharField(max_length=32,blank=True,null=True)
    def __str__(self):
        return self.scenario_writer
    class Meta:
        verbose_name_plural='Scenario Writer lists'

class GenreModel(models.Model):
    genre=models.CharField(max_length=64)
    yomigana=models.CharField(max_length=64)
    def __str__(self):
        return self.genre+' : '+ str(self.id)
    class Meta:
        ordering=['yomigana']
        verbose_name_plural='Genre lists'

class VoiceDataModel(models.Model):
    public_record_id=models.CharField(default=create_public_record_id, max_length=32)
    name=models.CharField(max_length=255)
    work_id=models.CharField(max_length=31)
    circle=models.ForeignKey(CircleModel,on_delete=models.SET_DEFAULT,default=1)
    release_date=models.DateField()
    add_date=models.DateField(default=datetime.now)
    character_voice=models.ManyToManyField(CharacterVoiceModel,blank=True)
    url=models.CharField(max_length=255,blank=True)
    url_af=models.CharField(max_length=255,blank=True)
    url_img=models.CharField(max_length=255,blank=True)
    commerce_switch=models.BooleanField(default=True)
    public_switch=models.BooleanField(default=True)
    public_delete=models.BooleanField(default=False)
    sample_switch=models.BooleanField(default=True)
    adult_switch=models.BooleanField(default=True)
    confidence=models.FloatField(default=100)
    display_range=models.IntegerField(default=100)
    genres=models.ManyToManyField(GenreModel,blank=True)
    scenario_writers=models.ManyToManyField(ScenarioWriterModel,blank=True,related_name='scenario_writers_many')
    description=models.TextField(blank=True,null=True)
    description_original=models.TextField(blank=True,null=True)
    description_conv=models.TextField(blank=True,null=True)
    chapter_names=models.CharField(max_length=4096,blank=True,null=True)
    maintext_original=models.TextField(blank=True,null=True)
    maintext=models.TextField()
    maintext_conv=models.TextField(blank=True,null=True)
    maintext_old=models.TextField(blank=True,null=True)
    text_version=models.CharField(blank=True,null=True,max_length=64)
    uid=models.CharField(max_length=64,default="",null=True,blank=True)


    def __str__(self):
        return self.name+' id:'+str(self.id)
    class Meta:
        verbose_name_plural="Voice Data lists"


class SearchLog(models.Model):
    keyword=models.CharField(max_length=100,default='None')
    ip_address=models.CharField(max_length=50,default='0.0.0')
    user=models.CharField(max_length=30,default='None')
    elapsed_time=models.FloatField(default=0)
    adddate=models.DateTimeField(auto_now_add=True)

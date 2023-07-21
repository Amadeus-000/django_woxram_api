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
    character_voice=models.CharField(max_length=20)
    yomigana=models.CharField(max_length=40,default="none")
    alias=models.CharField(max_length=127,blank=True,null=True)
    cv_link=models.CharField(max_length=64,default="",blank=True,null=True)
    def __str__(self):
        return self.character_voice
    class Meta:
        #verbose_name = "VoiceActor lists(VoiceactorModel)"
        verbose_name_plural = "character voice lists"
        ordering=['yomigana']

class CircleState(models.Model):
    state=models.CharField(max_length=255)
    def __str__(self):
        return self.state

class CircleState2(models.Model):
    state=models.CharField(max_length=255)
    def __str__(self):
        return self.state

class CircleModel(models.Model):
    circle=models.CharField(max_length=127)
    yomigana=models.CharField(max_length=127)
    alias=models.CharField(max_length=127,blank=True,null=True)
    circle_id=models.CharField(max_length=10,blank=True,null=True)
    url_circle=models.CharField(max_length=127,blank=True,null=True)
    publication_state=models.ForeignKey(CircleState,on_delete=models.CASCADE,default=1)
    approval_state=models.ForeignKey(CircleState2,on_delete=models.CASCADE,default=1)
    supplement=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.circle
    class Meta:
        verbose_name_plural="Circle lists"
        ordering=['yomigana']

class ScenarioWriterModel(models.Model):
    scenario_writer=models.CharField(max_length=30)
    yomigana=models.CharField(max_length=60)
    alias=models.CharField(max_length=127,blank=True,null=True)
    def __str__(self):
        return self.scenario_writer
    class Meta:
        verbose_name_plural='Scenario Writer lists'
        ordering=['yomigana']

class GenreModel(models.Model):
    genre=models.CharField(max_length=31)
    yomigana=models.CharField(max_length=31)
    def __str__(self):
        return self.genre+' : '+ str(self.id)
    class Meta:
        ordering=['yomigana']
        verbose_name_plural='Genre lists'

class OrderMenu(models.Model):
    menu=models.CharField(max_length=63)
    menucode=models.CharField(max_length=32,default='none')
    order=models.IntegerField()
    def __str__(self):
        return self.menu
    class Meta:
        ordering=['order']

class SearchInfoModel(models.Model):
    keyword=models.CharField(max_length=100)
    circle=models.ForeignKey(CircleModel,on_delete=models.CASCADE,default=1)
    character_voice=models.ForeignKey(CharacterVoiceModel,on_delete=models.CASCADE,default=1)
    order=models.ForeignKey(OrderMenu,on_delete=models.CASCADE,default=1)
    scenario=models.ForeignKey(ScenarioWriterModel,on_delete=models.CASCADE,default=1)
    sample_switch=models.BooleanField(default=True)
    create_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_DEFAULT,
        default=1,
    )

class WorkTextState(models.Model):
    name=models.CharField(max_length=32)
    code=models.CharField(max_length=32)
    description=models.CharField(max_length=64,blank=True,null=True)
    def __str__(self):
        return self.name

class VoiceDataModel(models.Model):
    public_record_id=models.CharField(default=create_public_record_id, max_length=25)
    name=models.CharField(max_length=255)
    work_id=models.CharField(max_length=31)
    circle=models.ForeignKey(CircleModel,on_delete=models.SET_DEFAULT,default=1)
    release_date=models.DateField()
    add_date=models.DateField(default=datetime.now)
    #author=models.CharField(max_length=100)
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
    # remark=models.CharField(max_length=255,blank=True,null=True)
    genres=models.ManyToManyField(GenreModel,blank=True)
    # scenario=models.ForeignKey(
    #     ScenarioWriterModel,
    #     on_delete=models.SET_DEFAULT,
    #     default=1,
    # )
    scenario_writers=models.ManyToManyField(ScenarioWriterModel,blank=True,related_name='scenario_writers_many')
    description=models.TextField(blank=True,null=True)
    description_original=models.TextField(blank=True,null=True)
    description_conv=models.TextField(blank=True,null=True)
    chapter_names=models.CharField(max_length=2048,blank=True,null=True)
    maintext_original=models.TextField(blank=True,null=True)
    maintext=models.TextField()
    maintext_conv=models.TextField(blank=True,null=True)
    maintext_old=models.TextField(blank=True,null=True)
    text_version=models.CharField(blank=True,null=True,max_length=64)
    # work_text_state = models.ForeignKey(
    #     WorkTextState,
    #     on_delete=models.SET_DEFAULT,
    #     default=1,
    # )
    # create_user = models.ForeignKey(
    #     get_user_model(),
    #     on_delete=models.SET_DEFAULT,
    #     default=1,
    # )

    def __str__(self):
        return self.name+' id:'+str(self.id)
    class Meta:
        verbose_name_plural="Voice Data lists"

class Upload_file(models.Model):
    file_txt = models.FileField(
        upload_to='uploads/',
        verbose_name='info.txt',
        validators=[FileExtensionValidator(['txt', ])],
    )
    file_txt2 = models.FileField(
        upload_to='uploads/',
        verbose_name='output.txt',
        validators=[FileExtensionValidator(['txt', ])],
        default=None,
    )

class Upload_file_zip(models.Model):
    file_zip = models.FileField(
        upload_to='uploads/',
        verbose_name='zipファイル',
        validators=[FileExtensionValidator(['zip', ])],
    )

class SearchLog(models.Model):
    keyword=models.CharField(max_length=100,default='None')
    ip_address=models.CharField(max_length=50,default='0.0.0')
    user=models.CharField(max_length=30,default='None')
    elapsed_time=models.FloatField(default=0)
    adddate=models.DateTimeField(auto_now_add=True)

class UserAccount(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_DEFAULT,
        default=1,
    )
    add_count=models.IntegerField(default=0)
    permission_addwork=models.BooleanField(default=True)
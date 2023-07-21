from django.db import models

class SearchExample(models.Model):
    url=models.CharField(max_length=255,default="")
    keyword=models.CharField(max_length=31,default="")
    def __str__(self):
        return self.keyword
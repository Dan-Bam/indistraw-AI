from django.db import models
from django.contrib.postgres.fields import ArrayField
class Genre_Data(models.Model):
    genre = ArrayField(models.CharField(max_length=20), blank=True)  # 영화 DB에서 가져오는 ID에 해당하는 장르
    movie_id = models.CharField(max_length=9999, primary_key=True)  # 영화 DB에서 가져오는 ID


class View_Record(models.Model):
    record = ArrayField(models.CharField(max_length=9990), blank=True)  # 계정 DB에서 가져오는 시청 기록값
    account_id = models.CharField(max_length=9999, primary_key=True)

class Default_Recommandation(models.Model):
    record = models.CharField(max_length=100)
class Recommandation(models.Model):
    account_id = models.ForeignKey(View_Record, on_delete=models.CASCADE, primary_key=True)
    record = ArrayField(models.CharField(max_length=2990), blank=True)
# Create your models here.

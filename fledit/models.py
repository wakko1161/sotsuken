from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.enums import Choices
from django.db.models.fields import DateField
from django.db.models.fields.related import ForeignKey, create_many_to_many_intermediary_model
from django.db.models.query_utils import FilteredRelation


# Create your models here.

class TripModel(models.Model):
    title = models.CharField(verbose_name='旅行名', max_length=100)
    tripid = models.AutoField(verbose_name='管理番号', primary_key=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    postdate = models.DateField(verbose_name='投稿日', auto_now_add=True)
    category = models.CharField(verbose_name='カテゴリ', max_length=50)
    tripdate = models.DateField(verbose_name='旅行日')
    budget = models.TextField(verbose_name='予算メモ', max_length=1000, blank=True)
    content = models.TextField(verbose_name='旅行メモ', max_length=2000, blank=True)
    images = models.ImageField(verbose_name='写真(1枚のみ)', blank=True, default="noimage.jpg")

    def __str__(self):
        return str("ID: ") + str(self.tripid) + str(" ") + self.title


class RootModel(models.Model):
    ROOTCHOICE = (('列車', '列車'), ('新幹線', '新幹線'), ('バス', 'バス'), ('タクシー', 'タクシー')
      , ('飛行機', '飛行機'), ('船', '船'), ('徒歩', '徒歩'), ('イベント', 'イベント'), ('その他', 'その他'))
    RTROOTCHOICE = (('列車', '列車'), ('新幹線', '新幹線'), ('バス', 'バス'), ('タクシー', 'タクシー')
      , ('飛行機', '飛行機'), ('船', '船'), ('徒歩', '徒歩'), ('その他', 'その他'))
    tripid = models.ForeignKey(TripModel, on_delete=models.CASCADE, verbose_name='旅行データ',
       related_name='related_root')
    depspot = models.CharField(verbose_name='出発地点/場所', max_length=50)
    arrspot = models.CharField(verbose_name='到着地点', max_length=50, blank=True)
    deptime = models.TimeField(verbose_name='出発時刻/開始時刻')
    arrtime = models.TimeField(verbose_name='到着時刻/終了時刻')
    earlydep = models.BooleanField(verbose_name='前日発/前日', blank=True)
    latearr = models.BooleanField(verbose_name='翌日着/翌日', blank=True)
    roottitle = models.CharField(verbose_name='行路/イベントのタイトル', max_length=50, blank=True)
    rootmemo = models.TextField(verbose_name='詳細メモ', max_length=1000, blank=True)
    rootcategory = models.CharField(verbose_name='行程カテゴリ', max_length=100)

    def __str__(self):
        return str(self.tripid) + str(" ") + self.depspot + str(" から ") + self.arrspot

class TodoModel(models.Model):
    PRIORITYCHOICE = (('必須', '必須'), ('優先', '優先'), ('普通', '普通'), ('優先でない', '優先でない'))
    tripid = models.ForeignKey(TripModel, on_delete=models.CASCADE, verbose_name='旅行データ',
        related_name='related_tdlist')
    rootid = models.ForeignKey(RootModel, on_delete=models.CASCADE, verbose_name='行程データ',
        related_name='related_root', null=True)
    tdtitle = models.CharField(verbose_name='ToDoタイトル', max_length=50)
    tdcontext = models.TextField(verbose_name='ToDo概要', max_length=1000, blank=True)
    tddid = models.BooleanField(verbose_name='完了済みか', blank=True)
    tdpriority = models.CharField(verbose_name='優先度', max_length=50)

    def __str__(self):
        return str(self.tripid) + str("の") + str(self.tdtitle)
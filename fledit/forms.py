from django import forms
from django.db.models import fields
from .models import TodoModel, TripModel, RootModel

class TripForm(forms.ModelForm):
    class Meta:
        model = TripModel
        fields = ('title', 'author', 'category', 'tripdate', 'budget', 'content', 'image')

    title = forms.CharField(label='旅行名', required=True, max_length=100)
    category = forms.CharField(label='カテゴリ', required=True, max_length=50)
    tripdate = forms.DateField(label='旅行日', required=True, input_formats=['%Y-%m-%d'])
    budget = forms.CharField(label='予算メモ', required=False, max_length=1000)
    content = forms.CharField(label='旅行メモ', required=False, max_length=2000)
    image = forms.ImageField(label='画像', required=False)

class RootForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tripid'].widget = forms.HiddenInput()

    class Meta:
        model = RootModel
        fields = ('tripid', 'depspot', 'arrspot', 'deptime', 'arrtime', 'earlydep', 'latearr',
             'roottitle', 'rootmemo', 'rootcategory')

    tripid = forms.ModelChoiceField(queryset=TripModel.objects.all(), label='旅行データ')
    depspot = forms.CharField(label='出発地点', required=True, max_length=50)
    arrspot = forms.CharField(label='到着地点', required=True, max_length=50)
    deptime = forms.TimeField(label='出発時刻', required=True)
    arrtime = forms.TimeField(label='到着時刻', required=True)
    earlydep = forms.BooleanField(label='前日発', required=False)
    latearr = forms.BooleanField(label='翌日着', required=False)
    roottitle = forms.CharField(label='行路のタイトル', required=False, max_length=50, initial='(例)各停新宿行き')
    rootmemo = forms.CharField(label='詳細メモ', required=False, max_length=1000)
    rootcategory = forms.ChoiceField(label='行程カテゴリ', required=True, choices = RootModel.RTROOTCHOICE)

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tripid'].widget = forms.HiddenInput()
        self.fields['rootcategory'].widget = forms.HiddenInput()

    class Meta:
        model = RootModel
        fields = ('tripid', 'roottitle', 'depspot', 'deptime', 'arrtime', 'earlydep', 'latearr',
             'rootmemo', 'rootcategory')

    tripid = forms.ModelChoiceField(queryset=TripModel.objects.all(), label='旅行データ')
    roottitle = forms.CharField(label='イベントのタイトル', required=False, max_length=50, initial='(イベント名)')
    depspot = forms.CharField(label='場所', required=True, max_length=50)
    deptime = forms.TimeField(label='開始時刻', required=True)
    arrtime = forms.TimeField(label='終了時刻', required=True)
    earlydep = forms.BooleanField(label='前日', required=False)
    latearr = forms.BooleanField(label='翌日', required=False)
    rootmemo = forms.CharField(label='詳細メモ', required=False, max_length=1000)
    rootcategory = forms.ChoiceField(label='行程カテゴリ', required=True, choices = RootModel.ROOTCHOICE)

class TodoForm(forms.ModelForm):
    def __init__(self, num=None, *args, **kwargs):
        super(TodoForm,self).__init__(*args,**kwargs)
        self.fields['tripid'].widget = forms.HiddenInput()

    class Meta:
        model = TodoModel
        fields = ('tripid', 'rootid', 'tdtitle', 'tdcontext', 'tddid', 'tdpriority')

    tripid = forms.ModelChoiceField(queryset=TripModel.objects.all(), label='旅行データ')
    rootid = forms.ModelChoiceField(queryset=RootModel.objects.all(), label='行程データ')
    tdtitle = forms.CharField(label='ToDoタイトル', required=True, max_length=50)
    tdcontext = forms.CharField(label='ToDo概要', required=False, max_length=1000)
    tddid = forms.BooleanField(label='完了済みか', required=False)
    tdpriority = forms.ChoiceField(label='優先度', required=False, choices = TodoModel.PRIORITYCHOICE)


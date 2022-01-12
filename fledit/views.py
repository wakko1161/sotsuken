from django import forms
from django.shortcuts import render, redirect
from .models import TodoModel, TripModel, RootModel
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .forms import RootForm, TripForm, EventForm, TodoForm

# Create your views here.
tripmodel = TripModel.objects.all()

def listview(request):
    object_list = TripModel.objects.all()
    template_name = 'list.html'
    return render(request, template_name, { 'object_list': object_list })

def signupview(request):
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        try:
            User.objects.create_user(username_data, '', password_data)
        except IntegrityError:
            return render(request, 'signup.html', {'error': 'このユーザーは既に登録されています。'})
    else:
        print(User.objects.all())
    return render(request, 'signup.html', {})

def loginview(request):
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        user = authenticate(request, username=username_data,\
             password=password_data)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login')
    return render(request, 'login.html', {})

def logoutview(request):
    logout(request)
    return redirect('login')

class TrDetail(DetailView):
    template_name = 'detail.html'
    model = TripModel

class TrCreate(CreateView):
    template_name = 'trcreate.html'
    form_class = TripForm
    success_url = reverse_lazy('list')

class TrDelete(DeleteView):
    template_name = 'trdelete.html'
    model = TripModel
    success_url = reverse_lazy('list')

class RtDelete(DeleteView):
    template_name = "rtdelete.html"
    model = RootModel
    success_url = reverse_lazy('list')

class EvDelete(DeleteView):
    template_name = "evdelete.html"
    model = RootModel
    success_url = reverse_lazy('list')

class TdDelete(DeleteView):
    template_name = "tddelete.html"
    model = TodoModel
    success_url = reverse_lazy('list')

class TrUpdate(UpdateView):
    template_name = 'trupdate.html'
    model = TripModel
    form_class = TripForm
    success_url = reverse_lazy('list')

class RtUpdate(UpdateView):
    template_name = 'rtupdate.html'
    model = RootModel
    form_class = RootForm
    success_url = reverse_lazy('list')

class EvUpdate(UpdateView):
    template_name = 'evupdate.html'
    model = RootModel
    form_class = EventForm
    success_url = reverse_lazy('list')

class TdUpdate(UpdateView):
    template_name = 'tdupdate.html'
    model = TodoModel
    form_class = TodoForm
    success_url = reverse_lazy('list')

def rtcreateview(request, pk):
    trip = TripModel.objects.get(tripid=pk)
    form_class = RootForm
    template_name = 'rtcreate.html'

    if request.method == 'POST':
        data = {}
        data.setdefault('tripid', TripModel.objects.get(pk=request.POST['tripid']))
        data.setdefault('depspot', request.POST['depspot'])
        data.setdefault('arrspot', request.POST['arrspot'])
        data.setdefault('deptime', request.POST['deptime'])
        data.setdefault('arrtime', request.POST['arrtime'])
        data.setdefault('earlydep', request.POST.get('earlydep'))
        data.setdefault('latearr', request.POST.get('latearr'))
        data.setdefault('roottitle', request.POST['roottitle'])
        data.setdefault('rootmemo', request.POST['rootmemo'])
        data.setdefault('rootcategory', request.POST['rootcategory'])

        model = RootModel()
        form = form_class(request.POST, instance=model, initial=data)

        if form.is_valid():
            object = form.save(commit=False)
            object.save()
        return redirect('list')
    else:
        default = {'tripid':TripModel.objects.get(pk=pk), 'earlydep':False, 'latearr':False}
        form = form_class(request.GET or None, instance=trip, initial=default)
        return render(request, template_name, {'form':form, 'trip':trip})

def evcreateview(request, pk):
    trip = TripModel.objects.get(tripid=pk)
    form_class = EventForm
    template_name = 'evcreate.html'

    if request.method == 'POST':
        data = {}
        data.setdefault('tripid', TripModel.objects.get(pk=request.POST['tripid']))
        data.setdefault('roottitle', request.POST['roottitle'])
        data.setdefault('depspot', request.POST['depspot'])
        data.setdefault('deptime', request.POST['deptime'])
        data.setdefault('arrtime', request.POST['arrtime'])
        data.setdefault('earlydep', request.POST.get('earlydep'))
        data.setdefault('latearr', request.POST.get('latearr'))
        data.setdefault('rootmemo', request.POST['rootmemo'])
        data.setdefault('rootcategory', request.POST['rootcategory'])

        model = RootModel()
        form = form_class(request.POST, instance=model, initial=data)

        if form.is_valid():
            object = form.save(commit=False)
            object.save()
        return redirect('list')
    else:
        default = {'tripid':TripModel.objects.get(pk=pk), 'earlydep':False, 'latearr':False, 'rootcategory':'イベント'}
        form = form_class(request.GET or None, instance=trip, initial=default)
        return render(request, template_name, {'form':form, 'trip':trip})

def tdcreateview(request, pk):
    trip = TripModel.objects.get(tripid=pk)
    form_class = TodoForm
    template_name = 'tdcreate.html'
    data = {}
    model = TodoModel()
    form = form_class(request.POST, instance=model, initial=data)
    form.fields['rootid'].queryset = RootModel.objects.filter(tripid=pk)

    if request.method == 'POST':
        data.setdefault('tripid', TripModel.objects.get(pk=request.POST['tripid']))
        data.setdefault('tdtitle', request.POST['tdtitle'])
        data.setdefault('tdcontext', request.POST['tdcontext'])
        data.setdefault('tddid', request.POST.get('tddid'))
        data.setdefault('tdpriority', request.POST['tdpriority'])

        if form.is_valid():
            object = form.save(commit=False)
            object.save()
        return redirect('list')
    else:
        default = {'tripid':TripModel.objects.get(pk=pk), 'tddid':False, 'tdpriority':'普通'}
        form = form_class(request.GET or None, instance=trip, initial=default)
        form.fields['rootid'].queryset = RootModel.objects.filter(tripid=pk)
        return render(request, template_name, {'form':form, 'trip':trip})
        

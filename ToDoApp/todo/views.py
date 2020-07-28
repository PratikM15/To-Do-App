from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from datetime import datetime, date

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .models import Task


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        usname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=usname, password=pwd)
        if user is not None:
            login(request, user)
            try:
                tasks = Task.objects.filter(username=user)
                if len(tasks) == 0:
                    return render(request, "login.html", {'user': user, 'empty': 'You have no task.'})
                return render(request, "login.html", {'tasks': tasks, 'user': user})
            except:
                tasks = {}
                return render(request, "login.html", {'user': user, 'empty': 'You have nothing todo.'})
    return render(request, "index.html", {'user': None, 'flag':0})


@csrf_exempt
def signup_user(request):
    if request.method == 'POST':
        usname = request.POST['username1']
        email = request.POST['email']
        pwd = request.POST['password1']
        try:
            try:
                user = User.objects.get(email=email)
                flag = 2
                if user is not None:
                    return render(request, "index.html", {'flag': flag, 'username': usname, 'email': email})
            except:
                user = User.objects.get(username=usname)
                flag = 1
                if user is not None:
                    return render(request, "index.html", {'flag': flag, 'username': usname, 'email': email})
        except:
            user = User.objects.create_user(
                username=usname,
                password=pwd,
                email=email
            )
            user.save()
            login(request, user)
            return render(request, "login.html", {'user': user, 'empty': 'You have nothing todo.'})
    return render(request, "index.html", {'user': None})


@csrf_exempt
def delete(request, task_id):
    if request.method == 'POST':
        user = request.user
        task_id = str(task_id)
        try:
            task = Task.objects.filter(username=user, task_id=task_id)
            task.delete()
            try:
                tasks = Task.objects.filter(username=user)
                for i, task in enumerate(tasks):
                    task.task_id = i + 1
                    task.save()

                if len(tasks) == 0:
                    return render(request, "login.html", {'user': user, 'empty': 'You have no task.'})
                return render(request, "login.html", {'tasks': tasks, 'user': user})
            except Exception as e:
                tasks = {}
                return render(request, "login.html", {'user': user, 'empty': 'You have nothing todo.'})
        except:
            return render(request, "login.html", {'user': user})
    return render(request, "index.html")




@csrf_exempt
def add(request):
    if request.method == "POST":
        user = request.user
        task = request.POST['task']
        deadline = request.POST['deadline']
        try:
            deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        except Exception as e:
            tasks = Task.objects.filter(username=user)
            arg = {'user': user, 'tasks': tasks}
            return render(request, 'login.html', arg)
        try:
            objects1 = Task.objects.filter(username=user)
            task_id = len(objects1) + 1
        except:
            task_id = 1
        obj = Task(task_id=task_id, username=user, task=task, deadline=deadline)
        obj.save()
        try:
            tasks = Task.objects.filter(username=user)
        except:
            tasks = {}
        return render(request, "login.html", {'tasks': tasks, 'user': user})
    return render(request, 'index.html')

def logout_user(request):
    user = request.user
    logout(request)
    return render(request, "index.html")

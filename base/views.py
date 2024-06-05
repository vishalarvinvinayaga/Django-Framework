from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Message , Topic, User
#from django.contrib.auth.models import User
from .forms import RoomForm, updateUserForm, MessageForm, MyUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm



# rooms = [
#     {'id':1, 'name':'lets learn python' },
#     {'id':2, 'name':'DATA STRUCTURE' },
#     {'id':3, 'name':'sql' },
# ]

def loginUser(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request,'Invalid Username or Password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            return redirect('home') if next_url==None else redirect(next_url)
        else:
            messages.error(request,'Invalid Username or Password')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request): 
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Error Occured while registration')
    context = {'form':form}
    return render(request, 'base/login_register.html', context)


#view for the home page
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__topic__icontains = q) |
                                Q(name__icontains = q) |
                                Q(description__icontains = q) 
                                
                                ) 
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    topics_count = topics.count()
    room_messages = Message.objects.filter(Q(room__topic__topic__icontains = q))[:5]
    context = {'rooms':rooms, 'topics':topics, 'roomcount':room_count,'room_messages':room_messages,'topicscount':topics_count}
    return render(request, 'base/home.html', context)


#view for the room page
def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        room_messages = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'rooms':room,'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html',context)

    
@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic_name = topic_name.lower()
        topic, created = Topic.objects.get_or_create(topic=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(topic=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})


@login_required(login_url = 'login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('room', pk = message.room.id)
    return render(request,'base/delete.html',{'obj':message})

@login_required(login_url = 'login')
def updateMessage(request,pk):
    message = Message.objects.get(id=pk)
    form = MessageForm(instance=message)
    if request.method == 'POST':
        message.body = request.POST.get('body')
        message.save()
        #return redirect('home')
    context = {'form':form}
    return render(request, 'base/update_message.html', context)

@login_required(login_url = 'login')
def profilePage(request, pk):

    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms, 'room_messages':room_messages,'topics':topics}

    return render(request, 'base/profile_page.html', context)

@login_required(login_url = 'login')
def updateUser(request):
    user = request.user
    form = updateUserForm(instance = user)
    if request.method == 'POST':
        form = updateUserForm(request.POST, request.FILES, instance= user)
        if form.is_valid():
            form.save()
            return redirect('profile-page', pk=user.id)
    context = {'forms':form}
    return render(request,'base/update_user.html',context)

def browseTopics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topic = Topic.objects.filter(topic__icontains = q)

    context = {'topics':topic}

    return render (request, 'base/topics.html', context)


def activityPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room_messages = Message.objects.filter(Q(room__topic__topic__icontains = q))[:5]
    context = {'room_messages':room_messages }

    return render(request, 'base/activity.html', context)
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Day, Region, Room, Location, Message, Sight, Tour, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.core.paginator import Paginator

# Create your views here.

# rooms = [
#     {'id':0,'name':'Let\'s learn some Django!'},
#     {'id':1,'name':'Let\'s learn some NumPy!'},
#     {'id':2,'name':'Let\'s learn some Pandas!'},
#     {'id':3,'name':'Let\'s learn some Tensorflow!'},
#     {'id':4,'name':'Let\'s learn some Rest-API!'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR password is wrong!!!")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
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
            messages.error(request, 'An error occurred during registration!')
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(region__name__icontains=q) |
        Q(name__icontains=q) 
        # Q(description__icontains=q)
    )
    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    locations = Region.objects.all()[0:7]
    locations_count = Region.objects.all().count()
    rooms_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__location__name__icontains=q)).order_by('-created')
    days = Day.objects.all()
    tours = Tour.objects.all()
    context = {'rooms': page_obj, 'locations': locations, 'rooms_count': rooms_count, 'room_messages': room_messages, 'tours': tours, 'days': days, 'locations_count': locations_count}
    return render(request, "base/home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, "base/room.html", context)

def tour(request, pk):
    tour = Tour.objects.get(id=pk)
    days = tour.days.all()
    context = {'tour': tour, 'days': days}
    return render(request, "base/tour.html", context)

def day(request, pk):
    day = Day.objects.get(id=pk)
    context = {'day': day}
    return render(request, "base/day.html", context)

def sight(request, pk):
    sight = Sight.objects.get(id=pk)
    context = {'sight': sight}
    return render(request, "base/sight.html", context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    locations = Region.objects.all()[0:7]
    locations_count = Region.objects.all().count()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'locations': locations, 'locations_count': locations_count}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    locations = Location.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        location, created = Location.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            location=location,
            name=request.POST.get('name'),
            description=request.POST.get('description'), 
        )
        return redirect('home')
    context = {'form': form, 'locations': locations}
    return render(request, "base/room_form.html", context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    locations = Location.objects.all()
    if request.user != room.host:
        return HttpResponse("You are not allowed here!!!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Location.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'locations': locations, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!!")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed here!!!")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    locations = Region.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'locations': locations})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

def toursPage(request):
    tours = Tour.objects.all()
    return render(request, 'base/tours.html', {'tours': tours}) 

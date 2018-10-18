from django.shortcuts import render, redirect, HttpResponse
from . models import *
import re
EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from django.contrib import messages
import bcrypt



def index(request):
    return render(request, 'first_app/index.html')

def register(request):
    if request.method !='POST':
        return redirect ('/')

    error=False

    if len(request.POST['first_name'])<2:
        messages.error(request, "First name must be greater than 2 characters")
        error=True
    if len(request.POST['password'])<5:
        messages.error(request, "Password must be greater than 5 characters")
        error=True
    if request.POST['password'] != request.POST['c_password']:
        messages.error(request, "Password must match")
        error=True
        return redirect ('/')
    else:
        if not EMAIL_REGEX.match(request.POST['email']):
            messages.error(request, "E-mail must be in appropriate format")
            error=True
        if len(User.objects.filter(email=request.POST['email']))>0: #the column email checking the email value from post form
            messages.error(request, "E-mail already taken")
            error=True
        if error:
            return redirect ('/')
        hashed_pw=bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        
        the_user=User.objects.create(first_name=request.POST['first_name'], email=request.POST['email'], password=hashed_pw)

        request.session['user_id']=the_user.id 

        return redirect('/wall')
        
def login(request):
    if request.method !='POST':
        return redirect ('/')
    try:
        the_user=User.objects.get(email=request.POST['email'])
    except:
        messages.error(request, "E-mail or password is invalid")
        return redirect ('/')
    if bcrypt.checkpw(request.POST['password'].encode(),the_user.password.encode()): request.session['user_id']=the_user.id 
    return redirect ('/wall')
    messages.error(request, "E-mail/password do not match")
    return redirect ('/')

def logout(request):
    request.session.clear()
    return redirect ('/')

def wall(request):
    if not 'user_id' in request.session:
        messages.error(request, "Redirected")
        return redirect ('/')
    context={
        "user":User.objects.get(id=request.session['user_id']),
        "messages": Message.objects.all(),
        "comments":Comment.objects.all(),
    
    }
    return render(request, 'first_app/wall.html', context)

def create_message(request):
    if not 'user_id' in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/wall')
    Message.objects.create(message=request.POST['message'], messenger=User.objects.get(id=request.session['user_id']))
    return redirect ('/wall')





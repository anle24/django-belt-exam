from django.shortcuts import render, redirect, HttpResponse
from .models import User, Quote
from django.contrib import messages
import bcrypt
from django.db.models import Count
# Create your views here.

def index(request):
    return render(request, 'finalbeltexam/index.html')


def process(request):
    if request.POST['action'] == 'register':
        postData = {
            "name": request.POST['name'],
            "alias": request.POST['alias'],
            "email": request.POST['email'],
            "password": request.POST['password'],
            "confirmpw": request.POST['confirmpw'],
            "birthday": request.POST['birthday']
        }
        validation = User.userManager.regVal(postData)
        if 'theUser' in validation:
            messages.success(request, "Successfully registered")
            return redirect('/')
        elif 'errors' in validation:
            for message in validation['errors']:
                messages.error(request, message)
            return redirect('/')
    elif request.POST['action'] == 'login':
        postData = {
            "email": request.POST['email'],
            "password": request.POST['password']
        }
        validation = User.userManager.login(postData)
        if 'theUser' in validation:
            if not 'user' in request.session:
                request.session['user'] =  validation['theUser'].id
            return redirect('/quotes')
        elif 'errors' in validation:
            for message in validation['errors']:
                messages.error(request, message)
            return redirect('/')

def logout(request):
    request.session.clear()
    messages.success(request, "You have logged out")
    return redirect('/')

def home(request):
    user = User.userManager.get(id = request.session['user'])
    context = {
        'user': user,
        'quotes': Quote.objects.exclude(favorites=user),
        'favorites': user.favorites.all()
    }
    return render(request, 'finalbeltexam/home.html', context)

def quote(request):
    user = User.userManager.get(id = request.session['user'])
    if request.POST['author'] < 4:
        messages.error(request, "Quoted by needs to be more than 3 characters")
    if request.POST['quote'] < 11:
        messages.error(request, "Quote needs to be more than 10 characters")
    elif request.POST['author'] > 3 and request.POST['quote'] > 10:
        Quote.objects.create(content = request.POST['quote'], author = request.POST['author'])
    return redirect('/quotes')

def userquotes(request, id):
    user = User.userManager.get(id = id)
    context = {
        "user": user,
        "posts": Quote.objects.filter(favorites=user)
    }
    return render(request, "finalbeltexam/user.html", context)

def favorite(request, id):
    this_user = User.userManager.get(id = request.session['user'])
    this_quote = Quote.objects.get(id = id)
    this_quote.favorites.add(this_user)
    return redirect('/quotes')

def removefavorite(request, id):
    this_user = User.userManager.get(id = request.session['user'])
    this_quote = Quote.objects.get(id = id)
    this_quote.favorite.remove(this_user)
    return redirect('/quotes')

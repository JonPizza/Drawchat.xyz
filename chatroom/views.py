from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

import random
import string
from glob import glob

def gen_rand_str():
    return ''.join([random.choice(string.ascii_letters) for _ in range(15)])

@login_required
def chat(request):
    if request.user.email.endswith('@xxxschoolemail.org'):
        return render(request, 'chat.html', {'code': request.user.profile.code})
    else:
        logout(request)
        return render(request, 'school_act.html')

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/chat/')
    else:    
        return render(request, 'login.html')

@login_required
def gallery(request):
    return render(request, 'gallery.html', {'dates': [i.split('/')[-1] for i in glob('/var/www/html/assets/images/*')]})

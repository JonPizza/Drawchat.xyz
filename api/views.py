from datetime import date
from glob import glob

from django.http import JsonResponse
from django.shortcuts import render
from .models import ChatMessage, Profile
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from .img import update_png, load_png, colors_reverse

IMG_DIR = '/var/www/html/assets/images/'

def school_email_required(f):
    def wrapper(request):
        if not request.user.email.endswith('@xxxschoolemail.org'):
            return JsonResponse({"success": False})
        return f(request)
    return wrapper

@login_required 
@school_email_required
def get_tick_data(request):
    msg_id = int(request.GET.get('msgId', None))
    if msg_id != None:
        chat_msgs = ChatMessage.objects.filter(pk__gt=msg_id)
        max_pk = chat_msgs.aggregate(Max('pk'))['pk__max']
        chat_msgs = list(ChatMessage.objects.filter(pk__gt=max_pk - 99)) if len(chat_msgs) > 100 else chat_msgs
        return JsonResponse({
            'msgs': [[c.message, c.sender, int(c.timestamp.timestamp())] for c in chat_msgs],
            'msgId': max_pk,
        })

@login_required
@school_email_required
def get_pixels(request):
    pixels = load_png(IMG_DIR + date.today().strftime('%b-%d-%Y.png'))[1]
    resp = {'pixels': []}
    for i in range(100):
        for j in range(100):
            px = pixels[i,j]
            if px != (255, 255, 255):
                resp['pixels'].append([f'{i}-{j}', colors_reverse[px]])
    return JsonResponse(resp)

@login_required
@school_email_required
def get_pixels_by_date(request):
    d = request.GET.get('date', date.today().strftime('%b-%d-%Y'))
    if '..' in d:
        return JsonResponse({'haha': 'very funny :) it would just be an empty array anyways'})

    pixels = load_png(IMG_DIR + d)[1]
    resp = {'pixels': []}
    for i in range(100):
        for j in range(100):
            px = pixels[i,j]
            if px != (255, 255, 255):
                resp['pixels'].append([f'{i}-{j}', colors_reverse[px]])
    return JsonResponse(resp)

def img(request):
    name = request.GET.get('name', 'Jonathan York')
    

def update_user_social_data(strategy, *args, **kwargs):
    response = kwargs['response']
    backend = kwargs['backend']
    user = kwargs['user']

    if response['picture']:
        url = response['picture']
        userProfile_obj = Profile()
        userProfile_obj.user = user
        userProfile_obj.picture = url
        userProfile_obj.save()

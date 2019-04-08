"""
Definition of views.
"""
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse,JsonResponse
from app.models import *
from django.contrib.auth import authenticate, login ,logout
import json
from django.contrib.sessions.models import Session

@csrf_exempt
def login_user(request):
    username = request.POST['name']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
        user_p=getUserProfile(user)
        login(request,user)
        return JsonResponse({'status':1, 'message': 'Successfully logged in', 'token': request.session.session_key})
    else:
        return JsonResponse({'status': 0, 'message': 'Invalid credentials'})
    
@csrf_exempt
def get_courtrooms(request):
    if request.method == "POST":
        try:
            session_key = request.POST['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except:
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)
        if isinstance(user_p,Judge):
            court_rooms  = [court_room for court_room in user_p.courtroom_set.all()]
        else:
            court_rooms = set()
            for judge in user_p.judge_set.all():
                court_rooms.update([court_room for court_room in  judge.courtroom_set.all()])
            court_rooms = list(court_rooms)
        
        def _get_bench(judges):
            return ', '.join([str(judge) for judge in judges])

        ret_court_rooms = [{'courtNumber': str(court_room.number), 
                            "roster": court_room.roster, 
                            "bench": _get_bench(court_room.judges.all())
                            } for court_room in court_rooms]

        return JsonResponse({'status' : 1, 'court_rooms': list(ret_court_rooms)})

def get_casefile_list(request):
    if request.method == "POST":
        try:
            session_key = request.POST['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except:
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)
        if isinstance(user_p,Judge):
            court_rooms  = [court_room for court_room in user_p.courtroom_set.all()]
        else:
            court_rooms = set()
            for judge in user_p.judge_set.all():
                court_rooms.update([court_room for court_room in  judge.courtroom_set.all()])
            court_rooms = list(court_rooms)

        return JsonResponse({'status' : 1, 'court_rooms': list(court_rooms)})


@csrf_exempt
def logout_user(request):
    logout(request)
    try:
        session_key = request.POST['session_key']
        session = Session.objects.get(session_key = session_key)
        session.delete()
    except:
        return JsonResponse({'status': 1, 'message': 'No user was logged in'})

    return JsonResponse({'status': 1, 'message': 'You have been successfully logged out'})

def getUserProfile(user):
    if user:
        try:
            user_p = Judge.objects.get(user = user)
        except:
            try:
                user_p = CourtStaff.objects.get(user = user)
            except:
                user_p = LR.objects.get(user = user)
    
    return user_p

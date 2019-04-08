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


@csrf_exempt
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

        data = request.data if request.data else request.form

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.objects.get(number=int(data['courtNumber']))
            except:
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.objects.get(number=int(data['courtNumber']))
                except:
                    pass
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        casefiles_response = []
        try:
            casefiles = court_room.casefile_set.all().filter(next_date_of_hearing=datetime.date.today())
            casefiles_response = [{"fileUploaded": casefile.file in not None,
                                    "itemNo": str(i),
                                    "caseNo": casefile.case_number,
                                    "matter": casefile.matter,
                                    "party": casefile.party,
                                    "lastHearingDate":casefile.last_date_of_hearing,
                                    "petitionerAdvocate":casefile.petitioner_advocate,
                                    "respondentAdvocate":casefile.respondent_advocate,
                                    "notes":casefile.notes,
                                    "type":casefile.case_type
                                } for i, casefile in enumerate(casefiles)]

        return JsonResponse({'status' : 1, 'court_rooms': casefiles_response})

@csrf_exempt
def get_casefile(request):
    if request.method == "POST":
        try:
            session_key = request.POST['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except:
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)

        data = request.data if request.data else request.form

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.objects.get(number=int(data['courtNumber']))
            except:
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.objects.get(number=int(data['courtNumber']))
                except:
                    pass
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        try:
            casefile = court_room.casefile_set.get(case_number=data['caseNo'])
        except:
            return JsonResponse({'status':0, 'message':'Casefile does not exist for user'})
        
        case_laws = [str(case_law) for case_law in casefile.case_laws]
        legislations = [str(legislature) for legislature in casefile.legislatures]

        casefile_response = {"caseNo": casefile.case_number,
                            "matter": casefile.matter,
                            "notes":casefile.notes,
                            "type":casefile.case_type,
                            "caselaws": case_laws,
                            "legislations": legislations
                        }

        return JsonResponse({'status' : 1, 'court_rooms': casefile_response})

@csrf_exempt
def get_file_stream(request):
    if request.method == "POST":
        try:
            session_key = request.POST['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except:
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)

        data = request.data if request.data else request.form

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.objects.get(number=int(data['courtNumber']))
            except:
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.objects.get(number=int(data['courtNumber']))
                except:
                    pass
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        try:
            casefile = court_room.casefile_set.get(case_number=data['caseNo'])
        except:
            return JsonResponse({'status':0, 'message':'Casefile does not exist for user'})
        
        if 'caselaw' in data:
            # Retrieve caselaw
            try:
                case_law = casefile.case_laws.objects.get(name = data['caselaw'])
                file = case_law.file
            except:
                return JsonResponse({'status':0, 'message':'Caselaw does not exist for user'})
        elif 'legislation' in data:
            # Retireve legislation
            try:
                legislature = casefile.legislatures.objects.get(name = data['legislation'])
                file = legislature.file
            except:
                return JsonResponse({'status':0, 'message':'Legislation does not exist for user'})
        else:
            # Retrieve casefile
            file = casefile.file
 
        filename = file.name.split('/')[-1]
        response = HttpResponse(file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response



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

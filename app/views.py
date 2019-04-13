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
    username = json.loads(request.body)['username']
    password = json.loads(request.body)['password']
    user = authenticate(username=username, password=password)
    if user:
        user_p=getUserProfile(user)
        login(request,user)
        return JsonResponse({'status':1, 'message': 'Successfully logged in',
                            'session_key': request.session.session_key, 'type': str(user_p.__class__.__name__), 'name': str(user_p.name)})
    else:
        return JsonResponse({'status': 0, 'message': 'Invalid credentials'})
    
@csrf_exempt
def get_courtrooms(request):
    if request.method == "POST":
        try:
            session_key = json.loads(request.body)['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(f"Error: {e}")
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
            session_key = json.loads(request.body)['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)

        data = json.loads(request.body)

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.get(number=int(data['courtNumber']))
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.get(number=int(data['courtNumber']))
                except Exception as e:
                    print(f"Error: {e}")
                    pass
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        casefiles_response = []
        try:
            casefiles = court_room.casefile_set.all()
            print([str(casefile) for casefile in casefiles])
            casefiles_response = [{"pk": casefile.pk,
                                    "fileUploaded": casefile.file is not None,
                                    "itemNo": str(i),
                                    "caseNumber": casefile.case_number,
                                    "matter": casefile.matter,
                                    "party": casefile.party,
                                    "lastHearingDate":casefile.last_date_of_hearing,
                                    "nextHearingDate":casefile.next_date_of_hearing,
                                    "petitionerAdvocate":casefile.petitioner_advocate,
                                    "respondentAdvocate":casefile.respondant_advocate,
                                    "notes":casefile.notes,
                                    "type":casefile.case_type,
                                    "status":casefile.status,
                                    "order_status":casefile.order_status,
                                    "is_urgent":casefile.is_urgent
                                } for i, casefile in enumerate(casefiles)]
        except Exception as e:
            print(e)
        return JsonResponse({'status' : 1, 'casefiles': casefiles_response})

@csrf_exempt
def get_casefile(request):
    if request.method == "POST":
        try:
            session_key = json.loads(request.body)['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)

        data = json.loads(request.body)

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.get(number=int(data['courtNumber']))
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.get(number=int(data['courtNumber']))
                except Exception as e:
                    print(f"Error: {e}")
                    pass
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        try:
            casefile = court_room.casefile_set.get(pk=data['casefile_pk'])
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Casefile does not exist for user'})
        
        case_laws = [{'name': str(case_law), 'pk': case_law.pk} for case_law in casefile.case_laws.all()]
        legislations = [{'name': str(legislature), 'pk': legislature.pk} for legislature in casefile.legislatures.all()]

        casefile_response = {"pk": casefile.pk,
                            "caseNumber": casefile.case_number,
                            "caselaws": case_laws,
                            "legislations": legislations
                        }

        return JsonResponse({'status' : 1, 'casefile': casefile_response})

@csrf_exempt
def get_file_stream(request):
    if request.method == "POST":
        try:
            session_key = json.loads(request.body)['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)

        data = json.loads(request.body)

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.get(number=int(data['courtNumber']))
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.get(number=int(data['courtNumber']))
                except Exception as e:
                    print(f"Error: {e}")
                    pass
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        try:
            casefile = court_room.casefile_set.get(pk=data['casefile_pk'])
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Casefile does not exist for CourtRoom'})
        
        if 'caselaw_pk' in data:
            # Retrieve caselaw
            try:
                case_law = casefile.case_laws.all().get(pk = data['caselaw_pk'])
                file = case_law.file
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Caselaw does not exist for Casefile'})
        elif 'legislation_pk' in data:
            # Retireve legislation
            try:
                legislature = casefile.legislatures.all().get(pk = data['legislation_pk'])
                file = legislature.file
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Legislation does not exist for Casefile'})
        elif 'peshi_pk' in data:
            # Retireve peshi
            try:
                # peshi = casefile.peshi
                # file = peshi.file
                peshi = casefile.peshi_char
                return JsonResponse({'status':1, 'peshi':peshi})
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Peshi does not exist for Casefile'})
        elif 'order_pk' in data:
            # Retireve order
            try:
                # order = casefile.order
                # file = order.file
                order = casefile.order_char
                return JsonResponse({'status':1, 'order':order})
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Order does not exist for Casefile'})
        else:
            # Retrieve casefile
            file = casefile.file
 
        file_name = file.name.split('/')[-1]
        file_path = file.path

        return JsonResponse({'status':1, 'file_name':file_name, 'file_path': file_path})

@csrf_exempt
def add_file(request):
    if request.method == "POST":
        try:
            session_key = json.loads(request.body)['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)

        data = json.loads(request.body)

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.get(number=int(data['courtNumber']))
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.get(number=int(data['courtNumber']))
                except Exception as e:
                    print(f"Error: {e}")
                    pass
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        
        files = request.FILES

        try:
            casefile = court_room.casefile_set.get(pk=data['casefile_pk'])
        except Exception as e:
            if 'casefile' in files:
                try:
                    case_number = data['casefile']['caseNumber']
                    matter = data['casefile']['matter']
                    party = data['casefile']['party']
                    last_date_of_hearing = data['casefile']['lastHearingDate']
                    next_date_of_hearing = data['casefile']['nextHearingDate']
                    petitioner_advocate = data['casefile']['petitionerAdvocate']
                    respondant_advocate = data['casefile']['respondentAdvocate']
                    type = data['casefile']['type']
                    status = data['casefile']['status']
                    is_urgent = data['casefile']['is_urgent']
                    file = files['casefile']
                    casefile = CaseFile.objects.get_or_create(case_number=case_number,
                                                              matter=matter,
                                                              party=party,
                                                              last_date_of_hearing=last_date_of_hearing,
                                                              next_date_of_hearing=next_date_of_hearing,
                                                              petitioner_advocate=petitioner_advocate,
                                                              respondant_advocate=respondant_advocate,
                                                              type=type,
                                                              status=status,
                                                              is_urgent=is_urgent,
                                                              file=file,
                                                              court_room=court_room)
                    return JsonResponse({'status':1, 'message':'CaseFile saved successfully.'})
                except Exception as e:
                    print(f"Error: {e}")
                    return JsonResponse({'status':0, 'message':'Error occured while saving CaseFile'})

        if 'caselaw' in files:
            # Retrieve caselaw
            try:
                name = data['caselaw']['name']
                file = files['caselaw']
                caselaw = CaseLaw.objects.get_or_create(file=file,
                                                          name=name)
                casefile.case_laws.add(caselaw)
                return JsonResponse({'status':1, 'message':'CaseLaw saved successfully.'})
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Error occured while saving Caselaw'})
        elif 'legislation' in files:
            # Retrieve legislation
            try:
                name = data['legislation']['name']
                file = files['legislation']
                legislation = Legislature.objects.get_or_create(file=file,
                                                          name=name)
                casefile.case_laws.add(legislation)
                return JsonResponse({'status':1, 'message':'Legislation saved successfully.'})
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Error occured while saving Legislation'})
        # elif 'peshi' in files:
        #     # Retireve peshi
        #     try:
        #         # peshi = casefile.peshi
        #         # file = peshi.file
        #         peshi = casefile.peshi_char
        #         return JsonResponse({'status':1, 'peshi':peshi})
        #     except Exception as e:
        #         print(f"Error: {e}")
        #         return JsonResponse({'status':0, 'message':'Peshi does not exist for Casefile'})
        # elif 'order' in files:
        #     # Retireve order
        #     try:
        #         # order = casefile.order
        #         # file = order.file
        #         order = casefile.order_char
        #         return JsonResponse({'status':1, 'order':order})
        #     except Exception as e:
        #         print(f"Error: {e}")
        #         return JsonResponse({'status':0, 'message':'Order does not exist for Casefile'})
        else:
            # Retrieve casefile
            return JsonResponse({'status':0, 'message':'No relevant file found'})
        return JsonResponse({'status':0, 'message':'Don\'t know how we reached this response. Debug. Have fun.'})

@csrf_exempt
def update_peshi(request):
    if request.method == "POST":
        try:
            session_key = json.loads(request.body)['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)

        data = json.loads(request.body)

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.get(number=int(data['courtNumber']))
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.get(number=int(data['courtNumber']))
                except Exception as e:
                    print(f"Error: {e}")
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        try:
            casefile = court_room.casefile_set.get(pk=data['casefile_pk'])
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Casefile does not exist for CourtRoom'})
        try:
            new_peshi_data = data['peshi']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new peshi data found'})
        try:
            casefile.peshi_char.update(new_peshi_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving peshi'})

        return JsonResponse({'status':0, 'message':'Peshi saved successfully'})

@csrf_exempt
def update_order(request):
    if request.method == "POST":
        try:
            session_key = json.loads(request.body)['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)

        data = json.loads(request.body)

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.get(number=int(data['courtNumber']))
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.get(number=int(data['courtNumber']))
                except Exception as e:
                    print(f"Error: {e}")
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        try:
            casefile = court_room.casefile_set.get(pk=data['casefile_pk'])
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Casefile does not exist for CourtRoom'})
        try:
            new_order_data = data['order']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new order data found'})
        try:
            casefile.order_char.update(new_order_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving order'})

        return JsonResponse({'status':0, 'message':'Order saved successfully'})


@csrf_exempt
def update_is_urgent(request):
    if request.method == "POST":
        try:
            session_key = json.loads(request.body)['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)

        data = json.loads(request.body)

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.get(number=int(data['courtNumber']))
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.get(number=int(data['courtNumber']))
                except Exception as e:
                    print(f"Error: {e}")
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        try:
            casefile = court_room.casefile_set.get(pk=data['casefile_pk'])
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Casefile does not exist for CourtRoom'})
        try:
            new_is_urgent_data = data['is_urgent']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new is_urgent data found'})
        try:
            casefile.is_urgent.update(new_is_urgent_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving is_urgent'})

        return JsonResponse({'status':0, 'message':'is_urgent saved successfully'})

@csrf_exempt
def update_notes(request):
    if request.method == "POST":
        try:
            session_key = json.loads(request.body)['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)

        data = json.loads(request.body)

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.get(number=int(data['courtNumber']))
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.get(number=int(data['courtNumber']))
                except Exception as e:
                    print(f"Error: {e}")
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        try:
            casefile = court_room.casefile_set.get(pk=data['casefile_pk'])
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Casefile does not exist for CourtRoom'})
        try:
            new_notes_data = data['notes']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new notes data found'})
        try:
            casefile.notes.update(new_notes_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving notes'})

        return JsonResponse({'status':0, 'message':'notes saved successfully'})

@csrf_exempt
def update_casefile_details(request):
    if request.method == "POST":
        try:
            session_key = json.loads(request.body)['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)

        data = json.loads(request.body)

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.get(number=int(data['courtNumber']))
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.get(number=int(data['courtNumber']))
                except Exception as e:
                    print(f"Error: {e}")
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        try:
            casefile = court_room.casefile_set.get(pk=data['casefile_pk'])
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Casefile does not exist for CourtRoom'})
        try:
            new_case_number_data = data['caseNumber']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new caseNumber data found'})
        try:
            casefile.case_number.update(new_case_number_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving caseNumber'})

        try:
            new_next_date_of_hearing_data = data['nextHearingDate']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new nextHearingDate data found'})
        try:
            new_last_date_of_hearing_data = casefile.last_date_of_hearing
            casefile.next_date_of_hearing.update(new_next_date_of_hearing_data)
            casefile.last_date_of_hearing.update(new_last_date_of_hearing_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving nextHearingDate'})

        try:
            new_status_data = data['status']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new status data found'})
        try:
            casefile.status.update(new_status_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving status'})

        try:
            new_party_data = data['party']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new party data found'})
        try:
            casefile.party.update(new_party_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving party'})

        try:
            new_petitioner_advocate_data = data['petitionerAdvocate']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new petitionerAdvocate data found'})
        try:
            casefile.petitioner_advocate.update(new_petitioner_advocate_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving petitionerAdvocate'})

        try:
            new_respondant_advocate_data = data['respondentAdvocate']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new respondentAdvocate data found'})
        try:
            casefile.respondant_advocate.update(new_respondant_advocate_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving respondentAdvocate'})

        try:
            new_status_data = data['status']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new status data found'})
        try:
            casefile.status.update(new_status_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving notes'})

        try:
            new_type_data = data['type']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new type data found'})
        try:
            casefile.type.update(new_type_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving type'})

        return JsonResponse({'status':0, 'message':'caseNumber saved successfully'})


@csrf_exempt
def update_order_status(request):
    if request.method == "POST":
        try:
            session_key = json.loads(request.body)['session_key']
            session = Session.objects.get(session_key = session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Kindly login first'})

        user_p=getUserProfile(user)

        data = json.loads(request.body)

        if isinstance(user_p,Judge):
            try:
                court_room  = user_p.courtroom_set.get(number=int(data['courtNumber']))
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        else:
            court_room = None
            for judge in user_p.judge_set.all():
                try:
                    court_room = judge.courtroom_set.get(number=int(data['courtNumber']))
                except Exception as e:
                    print(f"Error: {e}")
            
        if court_room is None:
            return JsonResponse({'status':0, 'message':'Court Room does not exist for user'})
        try:
            casefile = court_room.casefile_set.get(pk=data['casefile_pk'])
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Casefile does not exist for CourtRoom'})
        try:
            new_order_status_data = data['order_status']
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'No new order_status data found'})
        try:
            casefile.order_status.update(new_order_status_data)
        except:
            print(f"Error: {e}")
            return JsonResponse({'status':0, 'message':'Error occured while saving order_status'})

        return JsonResponse({'status':0, 'message':'order_status saved successfully'})


@csrf_exempt
def logout_user(request):
    logout(request)
    try:
        session_key = json.loads(request.body)['session_key']
        session = Session.all().get(session_key = session_key)
        session.delete()
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'status': 1, 'message': 'No user was logged in'})

    return JsonResponse({'status': 1, 'message': 'You have been successfully logged out'})

def getUserProfile(user):
    if user:
        try:
            user_p = Judge.objects.get(user = user)
        except Exception as e:
            print(f"Error: {e}")
            try:
                user_p = CourtStaff.objects.get(user = user)
            except Exception as e:
                print(f"Error: {e}")
                user_p = LR.objects.get(user = user)
    
    return user_p

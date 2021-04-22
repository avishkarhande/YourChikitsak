from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from website.models import UserDetails, DoctorDetails, Work, Slot, Zoom, PatientDetails, allPatients
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import requests
import math
import json
import base64
from time import time
from datetime import datetime, timedelta
from django.contrib import messages

# Create your views here.

def base64_encode(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def index(request):
    if request.user.is_authenticated:
        return redirect('indexlogin')
    return render(request, "index.html")

@login_required
def indexlogin(request):
    doctors = []
    users = User.objects.all()
    for user in users:
        userDetails = UserDetails.objects.filter(user = user).first()
        if userDetails is not None:
            if userDetails.is_doctor==True:
                list = []
                docD = DoctorDetails.objects.filter(user = user).first()
                list.append(userDetails)
                list.append(docD)
                new_list = docD.services.split(",")
                list.append(new_list)
                doctors.append(list)

    context = {'doctors':doctors}
    return render(request, "indexlogin.html", context)

def appointments(request):
    docD = DoctorDetails.objects.get(user = request.user)
    userD = UserDetails.objects.get(user = request.user)
    slot = Slot.objects.filter(docId = docD)
    patientlist = []
    for s in slot:
        l = []
        patient = PatientDetails.objects.get(user = s.patientId)
        l.append(patient)
        l.append(s)
        patientlist.append(l)
    context = {'docD':docD, 'userD':userD, 'slots':slot, 'patientlist':patientlist}
    return render(request, "appointments.html", context)

def my_patients(request):
    docD = DoctorDetails.objects.get(user = request.user)
    userD = UserDetails.objects.get(user = request.user)
    mypatient = allPatients.objects.filter(doctor = request.user)
    mypatients = []
    for patient in mypatient:
        if patient not in mypatients:
            mypatients.append(patient)
    context = {'docD':docD, 'userD':userD, 'patients':mypatients}
    return render(request, "my-patients.html", context)

def doctor_dashboard(request):
    user = request.user
    docD = DoctorDetails.objects.get(user = user)
    userD = UserDetails.objects.get(user = user)
    return render(request, "doctor-dashboard.html", {'docD':docD, 'userD':userD})

def doctor_profile_settings(request):
    docD = UserDetails.objects.get(user = request.user)
    docD.is_first_login = False
    docD.save()
    devD = UserDetails.objects.get(user = request.user)
    try:
        docD = DoctorDetails.objects.get(user=request.user)
    except DoctorDetails.DoesNotExist:
        docD = None
    if docD is not None:
        
        docD = DoctorDetails.objects.get(user = request.user)
        isdegree = 0
        if bool(docD.degree) == True:
            isdegree = 1
        else:
            isdegree = 0
        work = Work.objects.filter(user = request.user)
        context = {'docD':docD, 'devD':devD, 'work':work, 'isdegree':isdegree}
        return render(request, "doctor-profile-settings.html", context)

def logina(request):
    if request.user.is_authenticated:
        return redirect('indexlogin')
    return render(request, "login.html")

def login(request):
    if(request.method == "POST"):
        email = request.POST["email"]
        password = request.POST["password"]
        getUser = User.objects.filter(email=email).first();

        if getUser is None:
            messages.error(request, "Account Not Found!")
            return redirect('logina')
        user = authenticate(request, username=getUser.username, password=password)
        if user is not None:
            auth_login(request, user)
            docD = UserDetails.objects.get(user = getUser)
            if docD.is_doctor:
                if docD.is_first_login:
                    return redirect('doctor-profile-settings')
                else:
                    return redirect('redirecta')
            return redirect('redirecta')
        else:
            return redirect('logina')

def logout_view(request):
    logout(request)
    return redirect('logina')

def register(request):
    if(request.method == "POST"):
        fname = request.POST["fname"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        checkUser = User.objects.filter(username = username).first()
        checkUserEmail = User.objects.filter(email = email).first()
        if checkUser is not None:
            messages.error(request, "User with this Username Already Exists")
            return redirect('logina')
        if checkUserEmail is not None:
            messages.error(request, "User with this Email Already Exists")
            return redirect('logina')
        user = User.objects.create_user(username, email, password)
        user.save();
        additionaldetails = UserDetails(name = fname,user = user, is_doctor = False)
        additionaldetails.save();

        patient = PatientDetails(user = user, userD = additionaldetails)
        patient.save()
        messages.success(request, "Account Created Successfully!")
        return redirect('logina')
    return render(request, "register.html")

def docregister(request):
    if(request.method == "POST"):
        fname = request.POST["fname"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        flag = 0
        flag1 = 0
        user = User.objects.filter(username = username).first()
        if user :
            messages.error(request, "User with this Username Already Exists")
            return redirect('logina')
        user = User.objects.filter(email = email).first()
        if user :
            messages.error(request, "User with this Email Already Exists")
            return redirect('logina')
        
        user = User.objects.create_user(username, email, password)
        user.save();
        additionaldetails = UserDetails(name = fname,user = user, is_doctor = True)
        additionaldetails.save();

        usera = User.objects.get(username = username)
        DocD = DoctorDetails(user = usera)
        DocD.save()

        messages.success(request, "Account Created Successfully!")
        return redirect('logina')
    return render(request, "doctor-register.html")

def updateDocDetails(request):
    if request.method == "POST":
        user = User.objects.get(username = request.user.username)
        phone = request.POST["phone"]
        gender = request.POST["gender"]
        about = request.POST["about"]
        clinic_name = request.POST["clinic_name"]
        price = request.POST["price"]
        Specialization = request.POST["specialization"]
        services = request.POST['services']
        state = request.POST['state']
        country = request.POST['country']
        DocD = DoctorDetails.objects.get(user = request.user)
        DocD.phone = phone
        DocD.gender = gender
        DocD.about = about
        DocD.clinic_name = clinic_name
        DocD.price = price
        DocD.Specialization = Specialization
        DocD.services = services
        DocD.state = state
        DocD.country = country
        if 'degree' in request.FILES:
            DocD.degree = request.FILES['degree']

        DocD.save()
        return redirect("doctor-profile-settings")

def doctorProfile(request, slug):
    getUser = User.objects.get(username = slug)
    UserD = UserDetails.objects.get(user = getUser)
    docD = DoctorDetails.objects.get(user = getUser)
    lis = docD.services.split(',')
    specs = docD.Specialization.split(',')
    work = Work.objects.filter(user = getUser)
    return render(request, "doctor-profile.html", {'curr_user' : getUser, 'UserD':UserD, 'docD':docD, 'lis':lis, 'specs':specs, 'work':work})

def updatephoto(request):
    if request.method == "POST":
        docD = DoctorDetails.objects.get(user = request.user)
        if 'picture' in request.FILES:
            docD.dp = request.FILES['picture']
        docD.save()
        return redirect('doctor-profile-settings')

def add_work(request):
    if request.method == "POST":
        hospital = request.POST['hospital']
        start = request.POST['start']
        end = request.POST['end']
        work = Work(hospital=hospital, start=start, end = end, user = request.user)
        work.save()
        return redirect('doctor-profile-settings')
    return HttpResponse("Invalid Request")

def book_slot(request, slug):
    if request.method == "POST":
        date = request.POST['date']
        user = User.objects.get(username = slug)
        docId = DoctorDetails.objects.get(user = user)
        getSlots = Slot.objects.filter(docId = docId).filter(date = date)
        allSlots = ["02:00:00-02:20:00", "02:20:00-02:40:00", "02:40:00-03:00:00"]
        availableSlots = []
        list = []
        for s in getSlots:
            list.append(s.slot)
        for s in allSlots:
            if s not in list:
                availableSlots.append(s);
        docD = DoctorDetails.objects.get(user = user)
        context = {'date':date, 'getSlots':getSlots, 'availableSlots': availableSlots, 'docD':docD}
        return render(request, "getslots.html", context)
    else:
        user = User.objects.get(username = slug)
        docD = DoctorDetails.objects.get(user = user)
        context = {'docD':docD}
        return render(request,"book-slot.html", context)

def addappointment(request, slug):
    slot = request.POST['slot']
    date = request.POST['date']
    user = User.objects.get(username = slug)
    docId = DoctorDetails.objects.get(user = user)
    patientId = request.user
    


def zoom_callback(request):
    code = request.GET["code"]
    print(code)
    data = requests.post(f"https://zoom.us/oauth/token?grant_type=authorization_code&code={code}&redirect_uri=http://127.0.0.1:8000/zoom/callback/", headers={
        "Authorization": "Basic " + base64_encode("Ft9VmHdcQSK9VkhHF6l6w:Ab04Axx97W8jDH2Y1vlplE768ImvE024"), "Content-Type": "application/json"
    })
    print(data.json())
    access_token = data.json()["access_token"]
    token_type = data.json()["token_type"]
    refresh_token = data.json()["refresh_token"]
    user = request.user
    expires = datetime.now() + timedelta(seconds=data.json()["expires_in"])
    scope = data.json()["scope"]
    zzoom = Zoom.objects.filter(user = user).first()
    if zzoom is not None:
        zzoom.access_token = access_token
        zzoom.token_type = token_type
        zzoom.refresh_token = refresh_token
        zzoom.user = user
        zzoom.expires = expires
        zzoom.scope = scope
        zzoom.save()
    else:
        zzoom = Zoom(access_token=access_token, token_type=token_type, refresh_token=refresh_token,user=user,expires=expires,scope=scope)
        zzoom.save()
    return redirect("indexlogin")


def addMeeting(request, slug):
    if request.method == "POST":
        slot = request.POST['slot']
        date = request.POST['date'] 
        user = User.objects.get(username = slug)
        docId = DoctorDetails.objects.get(user = user)
        patientId = request.user
        zoom_token = Zoom.objects.get(user = request.user).access_token
        zoom = Zoom.objects.get(user = request.user)
        expire_dt = Zoom.objects.get(user = request.user).expires
        print(zoom.refresh_token)
        dataa = requests.post("https://zoom.us/oauth/token?grant_type=refresh_token&refresh_token=" + zoom.refresh_token, headers={
            "content-type": "application/json",
            "authorization": "Basic " + base64_encode("Ft9VmHdcQSK9VkhHF6l6w:Ab04Axx97W8jDH2Y1vlplE768ImvE024")
        })

        print("Second")
        print(dataa.json())
        access_token = dataa.json()["access_token"]
        token_type = dataa.json()["token_type"]
        refresh_token = dataa.json()["refresh_token"]
        user = request.user
        expires = datetime.now() + timedelta(seconds=dataa.json()["expires_in"])
        scope = dataa.json()["scope"]
        zzoom = Zoom.objects.get(user = user)
        zzoom.access_token = access_token
        zzoom.token_type = token_type
        zzoom.refresh_token = refresh_token
        zzoom.user = user
        zzoom.expires = expires
        zzoom.scope = scope
        zzoom.save()
        usera = User.objects.get(username = slug)
        #print(zoom_tok)
        a = slot[:8]
        if usera == patientId:
            return HttpResponse("Failed Request")
        else:
            data = requests.post("https://api.zoom.us/v2/users/me/meetings", headers={
                'content-type': "application/json",
                "authorization": "Bearer " + str(zzoom.access_token)
            }, data=json.dumps({
                "topic": f"Interview with Me",
                "type": 2,
                "start_time": date + "T" + a + "Z",
            }))
            print(a)
            print(data.json()["join_url"], data.json()["start_url"])
            sl = Slot(slot = slot, date=date, docId = docId, patientId = patientId, startUrl = data.json()["start_url"], meetUrl = data.json()["join_url"])
            sl.save()
            user = User.objects.get(username = slug)
            patient = UserDetails.objects.get(user = request.user)
            allpatient = PatientDetails.objects.get(userD = patient)
            allpatient.save()
            name = User.objects.get(username = slug)
            allist = allPatients.objects.filter(patient = allpatient).first()
            if allist is None:
                alllist = allPatients(doctor=name, patient=allpatient)
                alllist.save()
            else :
                pass
            messages.success(request, "Appointment Scheduled Successfully")
            return redirect('patient-appointment')

def redirecta(request):
    return render(request, 'redirect.html')


def dashboardPatient(request):
    if request.method == "GET":
        patient = PatientDetails.objects.get(user = request.user)
        userD = UserDetails.objects.get(user = request.user)
        context = {'patient':patient,'userD':userD}
        return render(request, "dashboard.html", context)
    else:
        if 'dp' in request.FILES:
            dp = request.FILES['dp']
        state = request.POST['state']
        country = request.POST['country']
        phone = request.POST['phone']
        userD = UserDetails.objects.get(user = request.user)
        pat = PatientDetails.objects.filter(user = request.user).first()
        if pat is None:
            patient = PatientDetails(user = user,userD=userD,  state = state, country=country, phone=phone)
        else:
            pat.state = state
            pat.country = country
            pat.phone = phone
        if 'dp' in request.FILES:
            pat.dp = request.FILES['dp']
        pat.save()
        return redirect('dashboard')

def patient_appointment(request):
    allappointments = Slot.objects.filter(patientId=request.user)
    patient = PatientDetails.objects.get(user = request.user)
    list = []
    for a in allappointments:
        doctorDetails = a.docId
        docUser = UserDetails.objects.get(user = doctorDetails.user)
        n = []
        n.append(doctorDetails)
        n.append(docUser)
        n.append(a)
        list.append(n)
    context = {'appointments':list, 'patient':patient}
    return render(request, "patient-appointments.html", context)
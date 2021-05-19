"""consultDocOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('appointments', views.appointments, name="appointments"),
    path('my-patients', views.my_patients, name="my-patients"),
    path('doctor-dashboard', views.doctor_dashboard, name="doctor-dashboard"),
    path('doctor-profile-settings', views.doctor_profile_settings, name="doctor-profile-settings"),
    path('logina', views.logina, name="logina"),
    path('register', views.register, name="register"),
    path('docregister', views.docregister, name="docregister"),
    path('indexlogin', views.indexlogin, name="indexlogin"),
    path('login', views.login, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('updateDocDetails', views.updateDocDetails, name="updateDocDetails"),
    path('doctor/profile/<slug:slug>', views.doctorProfile, name="docprofile"),
    path('dashboard', views.dashboardPatient, name="dashboard"),
    path('updatephoto', views.updatephoto, name="updatephoto"),
    path('add-work', views.add_work, name="add-work"),
    path('book-slot/<slug:slug>', views.book_slot, name="book-slot"),
    path('add-appointment/<slug:slug>', views.addappointment, name="add-appointment"),
    path('zoom/callback/', views.zoom_callback, name="zoom-call"),
    path('addmeeting/<slug:slug>', views.addMeeting, name="addmeeting"),
    path('redirecta/', views.redirecta, name="redirecta"),
    path('patient-appointment/', views.patient_appointment, name="patient-appointment"),
    path('add-prescription/<slug:slug>', views.add_prescription, name="add-prescription"),
    path('view-prescription/<slug:slug>', views.view_prescription, name="view-prescription"),
    path('patientprescription/<slug:slug>', views.patientprescription, name="patient-prescription"),
    path('delete/<int:id>', views.delete_appointment, name="delete-appointment"),
    path('search', views.search, name="search"),
]

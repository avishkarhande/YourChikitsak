from django.contrib import admin
from website.models import UserDetails, DoctorDetails, Work, Slot, Zoom, allPatients, PatientDetails

# Register your models here.


admin.site.register(Work)

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_doctor', 'is_first_login')

admin.site.register(UserDetails, UserDetailsAdmin)

class DoctorDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified', 'mark')

class SlotAdmin(admin.ModelAdmin):
    list_display = ('docId', 'patientId', 'slot', 'date', 'meetUrl')

admin.site.register(Slot, SlotAdmin)

admin.site.register(DoctorDetails, DoctorDetailsAdmin)

admin.site.register(Zoom)

admin.site.register(allPatients)

admin.site.register(PatientDetails)
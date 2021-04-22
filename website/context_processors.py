from website.models import UserDetails

def add_variable_to_context(request):
    #print(request.user)
    if request.user.is_superuser:
        return {
            'is_doctor':0
        }
    elif not request.user.is_anonymous:
        getDetails = UserDetails.objects.get(user = request.user)
        return {
            'is_doctor':getDetails.is_doctor
        }
    else :
        return {
            'is_doctor':0
        }
    
    
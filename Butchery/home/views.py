from django.shortcuts import render

# Create your views here.
# Create your views here.
def home(request):

    context = {}
    return render(request, 'home/index.html', context)

def contact(request):
    if request.method == 'POST':
        message = request.POST['message']
        if request.user.is_authenticated:
            name = request.user.first_name + request.user.last_name
            email = request.user.email
            message = name + "\n" + email + "\n"+ message
            send_mail('Contact Form', message, settings.EMAIL_HOST_USER, ['django10.foxx@gmail.com', 'mcn10.foxx@gmail.com'], fail_silently="false" )
            messages.success(request, ("Your message has been sent successfully..."))
        else:
            name = request.POST['name']
            email = request.POST['email']
            message = name + "\n" + email + "\n"+ message
            send_mail('Contact Form', message, settings.EMAIL_HOST_USER, ['django10.foxx@gmail.com', 'mcn10.foxx@gmail.com'], fail_silently="false" )
            messages.success(request, ("Your message has been sent successfully..."))
        return redirect('home:home')

    return render(request, 'home/contact.html', {})

def profile(request):
    if request.user.is_authenticated:

        return render(request, 'home/profile.html', {})
    else:
        return redirect('home:home')



def edit_profile(request):
    if request.user.is_authenticated:
        return render(request, 'home/edit_profile.html', context)

    else:
        return redirect('account:login')

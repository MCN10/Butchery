from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from .forms import CreateUserForm, CustomerForm

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

from store.models import *

from .decorators import *


# Create your views here.\

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data['username']
                firstname = form.cleaned_data['first_name']
                lastname = form.cleaned_data['last_name']
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                group = Group.objects.get(name='customer')

                user = authenticate(request, username=username, password=password)
                login(request, user)

                Customer.objects.create(
                    user=user,
                    email=email,
                    firstname=firstname,
                    lastname=lastname,
                )
                messages.success(request, ('Registration Successful'))
                return redirect('store')

        else:
            form = CreateUserForm()
        context = {'form':  form}
        return render(request, 'account/register.html', context)









def profile(request):
    if request.user.is_authenticated:
        orders = request.user.customer.order_set.all()

        print('ORDERS: ', orders)
        context = {'orders': orders }
        return render(request, 'account/profile.html', context)
    else:
        return redirect('store')










login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out successfully..."))
    return redirect ('store')




def edit_profile(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        form = CustomerForm( instance=customer )
        print(Customer)
        if request.method == 'POST':
            form = CustomerForm(request.POST, request.FILES, instance=customer)
            if form.is_valid():
                form.valid()
                messages.success(request, ('Profile Updated Successfully'))


        context = {'form': form}
        print(context)
        print(request)
        return render(request, 'account/edit_profile.html', context)

    else:
        return redirect('account:login')



def loginPage(request):
    if request.user.is_authenticated:
            return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ("You are now logged in."))
                return redirect('store')
            else:
                messages.success(request, ("Error! Please try again..."))
                return redirect('account:login')
        else:
            return render(request, 'account/login.html', {})






login_required(login_url='login')
def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, ('Your password has been successfully updated!'))
                return redirect('store')
        else:
            form = PasswordChangeForm(user=request.user)
        context = {'form':  form}
        return render(request, 'account/change_password.html', context)

    else:
        return redirect('account:login')

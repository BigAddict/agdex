from django.db import utils
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        try:    
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname

            myuser.save()

            messages.success(request, "Your Account has been successfully been created")

        except utils.IntegrityError:
            messages.error(request, "The user is already registered! Please login to continue to your account.")
        except Exception as e:
            print("This error occurred!!")
        return redirect('signin')

    return render(request, "user_management/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            next_url = request.GET.get('next')
            if next_url:
                # Redirect to the specified 'next' URL
                return redirect(next_url)
            else:
                # If 'next' is not available, redirect to a default URL
                return redirect('/')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('signin')

    return render(request, "user_management/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('/auth')
from django.shortcuts import render, redirect

#Django authentication libraries           
from django.contrib.auth import authenticate, login, logout
#Django Form for authentication
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User 
   

#define a function view called login_view that takes a request from user
def login_view(request):
    #initialize:
    #error_message to None                                 
    error_message = None   
    #form object with username and password fields                             
    form = AuthenticationForm()     

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        #check if form is valid
        if form.is_valid():                                
            username = form.cleaned_data.get('username')      #read username
            password = form.cleaned_data.get('password')    #read password
            #use Django authenticate function to validate the user
            user = authenticate(username=username, password=password)
            if user is not None:                    #if user is authenticated
                #then use pre-defined Django function to login
                login(request, user)                
                return redirect('recipes:home') #& send the user to desired page
        
        # If we get here, authentication failed or form was invalid
        error_message = 'Invalid username or password'

    #prepare data to send from view to template
    context = {'form': form, 'error_message': error_message}
    return render(request, 'auth/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    form = UserCreationForm()
    error_message = None
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('recipes:home')
        else:
            error_message = 'Registration failed. Please correct the errors below.'
    return render(request, 'auth/register.html', {'form': form, 'error_message': error_message})
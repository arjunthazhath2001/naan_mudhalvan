from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    if request.method == "POST":
        # Get the username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user with the provided credentials
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            # Redirect the user to the index page after login
            return redirect('index')
        else:
            # If authentication fails, display an error message
            messages.error(request, "Invalid username or password")
    
    # Render the login page
    return render(request, 'placement_team_app/login.html')


# Index view with login protection
@login_required(login_url='login')  # Ensure the correct login URL
def index(request):
    return render(request, 'placement_team_app/index.html')
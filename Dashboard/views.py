from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import User
# from .models import User
# Create your views here.
def dashboard(request):
	if 'id' not in request.session:
		messages.error(request, "Please sign in to your account to continue!")
		return redirect("/signin")
	context = { 'users': User.userManager.getAllUsers() }
	return render(request, "dashboard.html", context)

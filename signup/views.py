from django.shortcuts import render,redirect
from signup import forms as f

# Create your views here.
def signup(response):
    if response.method == "POST":
        form = f.RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
	       form = f.RegisterForm()
    return render(response,'signup.html',{"form":form})

from django.shortcuts import render, redirect
from accounts.forms import UserAdminCreationForm


def login(request):
    return render(request, 'registration/login.html')


def register(req):
    form = UserAdminCreationForm()
    if req.method == 'POST':
        form = UserAdminCreationForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(req, 'registration/signup.html', {'form': form})

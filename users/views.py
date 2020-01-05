from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def register(request):
    #Register a new user
    if request.user.is_authenticated:
        messages.info(request, 'Your are already logged in!')
        return redirect('f_b:index')
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Log the user in and redirect to homepage
            login(request, new_user)
            return redirect('f_b:index')
    context = {'form':form}
    return render(request, 'registration/register.html', context)


from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.http import HttpResponse
# Create your views here.


def register(request):
    if request.method == 'POST':
        #Get form Values 
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        #check if password match
        if password == confirm_password:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request,"Bu foydalanuvchi nomi mavjud")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,"Bu elektron pochta foydalanilmoqda.")
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    messages.success(request,'Siz hozir ro`yxatdan o`tdingiz va tizimga kirishingiz mumkin')
                    return redirect('login')
        else:
            messages.error(request, "Parol mos kelmadi.")
            return redirect('register')
    else:
        return render(request,'users/registration.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            #messages.success(request,'You are Now Logged in')
            return redirect('dashboard')
        else:
            messages.error(request,"Hisob ma'lumotlari noto'g'ri")
            return redirect('login')
    else:
       return render(request,'users/login.html') 
    


def dashboard(request):
    return HttpResponse("dashboard")
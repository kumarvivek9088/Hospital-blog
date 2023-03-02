from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .models import User,Doctor,Patient, Blog
from django.contrib import messages
from django.db.models import Max
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        context = {"details":user}
        if user.is_patient==True:
            return render(request,'patienthome.html',context=context)
        if user.is_doctor==True:
            return render(request,"doctorhome.html",context=context)
        else:
            return render(request,"home.html")
    else:
        return redirect('/signin')

def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=="POST":
            username=request.POST['username']
            password=request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("/home")
            else:
                return redirect("/signin")
        else:
            return render(request,"login.html")

def doctorsignup(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=="POST":
            username = request.POST['username']
            password = request.POST['password']
            confpassword = request.POST['confirmpassword']
            if password==confpassword:
                user = User.objects.create_user(username=username,password=password)
                user.save()
                login(request,user)
                user = User.objects.get(username=username)
                email = request.POST['email']
                user.is_doctor=True
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                user.email=email
                user.first_name=firstname
                user.last_name=lastname
                user.save()
                profilepic = request.FILES['pic']
                adrs = request.POST['line1']
                city = request.POST['city']
                state = request.POST['state']
                pincode = request.POST['pincode']
                doc = Doctor(user=request.user,profilepic=profilepic,line1 = adrs ,city =city,state=state,pincode=pincode)
                doc.save()
                return redirect('/')
            else:
                return redirect('/signup/doctor')
        else:   
            return render(request,"doctorsignup.html")
def patientsignup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=="POST":
            username = request.POST['username']
            password = request.POST['password']
            confpassword = request.POST['confirmpassword']
            if password==confpassword:
                user = User.objects.create_user(username=username,password=password)
                user.save()
                login(request,user)
                user = User.objects.get(username=username)
                email = request.POST['email']
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                user.is_patient=True
                user.email=email
                user.first_name=firstname
                user.last_name=lastname
                user.save()
                profilepic = request.FILES['pic']
                adrs = request.POST['line1']
                city = request.POST['city']
                state = request.POST['state']
                pincode = request.POST['pincode']
                doc = Doctor(user=request.user,profilepic=profilepic,line1 = adrs ,city =city,state=state,pincode=pincode)
                doc.save()
                return redirect('/')
            else:
                return redirect('/signup/patient')
        else:   
            return render(request,"patientsignup.html")

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/signin")
    else:
        return redirect('/')
    
def upload(request):
    if request.user.is_authenticated and request.user.is_doctor:
        if request.method == "POST":
            title = request.POST['title']
            image = request.FILES['image']
            summary = request.POST['summary']
            content = request.POST['content']
            publish = request.POST['publish']
            category = request.POST['category']
            blognumber = Blog.objects.aggregate(Max('bno'))
            if blognumber['bno__max'] == None: #this is when blog model has no data and first time it will get data to save , in that case blognumber max initial be empty and a None
                newblog = Blog(bno = 1, user=request.user,title=title, image=image,category=category,summary=summary,content=content, public = publish)
                newblog.save()
            else:
                blognumber = blognumber['bno__max']+1
                newblog = Blog(bno = blognumber, user=request.user,title=title, image=image,category=category,summary=summary,content=content, public = publish)
                newblog.save()
            if publish=="True":
                messages.success(request,"Your blog upload successfully and publish")
                return render(request,"upload.html")
            else:
                messages.success(request,"Your blog upload successfully and saved as draft")
                return render(request,"upload.html")
                
        else:
            return render(request,"upload.html")
    else:
        return redirect('/')
        
def blog(request):
    if request.user.is_authenticated:
        data = Blog.objects.all().filter(public=True)
        context = {'data':data ,'fl' :'all'}
        return render(request,"blog.html",context=context)
    else:
        return redirect('/signin')
def myblog(request):
    if request.user.is_authenticated and request.user.is_doctor:
        data = Blog.objects.all().filter(user=request.user)
        context = {'data':data ,'fl':'all'}
        return render(request,'myblog.html',context=context)
    else:
        return redirect('/blog')
def filter(request,fl):
    if request.user.is_authenticated:
        if fl=="all":
            data = Blog.objects.all().filter(public=True)
            context = {'data':data , 'fl' : 'all'}
            return render(request,"blog.html",context=context)
        else:
            data = Blog.objects.all().filter(public=True,category=fl)
            context = {'data' : data , 'fl' : fl}
            return render(request,"blog.html",context=context)
    else:
        return redirect('/')
def myfilter(request,fl):
    if request.user.is_authenticated and request.user.is_doctor:
        if fl=="all":
            data = Blog.objects.all().filter(user=request.user)
            context = {'data':data , 'fl' : 'all'}
            return render(request,"myblog.html",context=context)
        else:
            data = Blog.objects.all().filter(user=request.user,category=fl)
            context = {'data' : data , 'fl' : fl}
            return render(request,"myblog.html",context=context)
    else:
        return redirect('/')
        
def viewblog(request,bno):
    if request.user.is_authenticated:
        data = Blog.objects.all().filter(bno=bno,public=True)
        context = {'data':data}
        return render(request,"viewblog.html",context=context)
    else:
        return redirect('/')
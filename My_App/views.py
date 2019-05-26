from django.shortcuts import render
from .models import User, ImageUpload
from django.contrib.auth import signals
#from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from .forms import AuthenticationForm, RegistrationForm

from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import login as django_login, logout as django_logout, authenticate as django_authenticate
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView, UpdateView
from .models import User
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.shortcuts import render

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = django_authenticate(email=email, password=password)
            if user is not None:
                if user.is_active and user.is_staff:
                    django_login(request,user)
                    return redirect('/dashboard') #user is redirected to dashboard
                else:
                    django_login(request,user)
                    return redirect('/dashboard2')
            else:
                form = AuthenticationForm()
                return render(request,'My_App/login.html',{'form':form,'error':'Incorrent Email and Password Try Again!'})
    else:
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('/dashboard')
        elif request.user.is_authenticated:
            return redirect('/dashboard2')
        form = AuthenticationForm()

    return render(request,'My_App/login.html',{'form':form,})


def register(request):
    if request.method == 'POST':
        def get_client_ip(request):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
        ip=get_client_ip(request)
        print(ip,'testing post methond')
        import geoip2.database
        reader = geoip2.database.Reader('./GeoLite2-Country_20190521/GeoLite2-Country.mmdb')
        try:
            response = reader.country(ip)
            location = response.country.iso_code
        except :
            location = "India"
        request.location =location
        print(request.location,'request modify')
        reader.close()

        form = RegistrationForm(data = request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password1']
            location = request.location

            print(location,'isvalid')


            user = form.save()
            test = User.objects.get(email=email)
            print(test,'test object get')
            User.objects.filter(email=email).update(location=location)
            print(user,'printing users')
            return redirect('/login')
    else:

        form = RegistrationForm()

    return render(request,'My_App/signup.html',{'form':form,})

def logout(request):
    django_logout(request)
    form = AuthenticationForm()
    return render(request,'My_App/home.html',{'form':form,})

@login_required(login_url ="/")
def dashboard(request):
    list_user = User.objects.all()

    return render(request, 'My_App/admin.html',{'data':list_user})


@login_required(login_url ="/")
def dashboard2(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/dashboard')
    else:
        email = request.user
        list_images = ImageUpload.objects.filter(email=email)
        return render(request, 'My_App/user.html',{'list_images':list_images})

@login_required
def userimage(request,id=None):
    getdata = get_object_or_404(User, id=id)
    email = getdata.id
    print(email)
    email = str(email)
    data = ImageUpload.objects.filter(email=email)
    return render(request,'My_App/admusr.html',{'data':data})

from django.views.generic.edit import UpdateView
from django.urls import reverse

class UpdateComment(UpdateView):
    model = ImageUpload
    fields = ['comment']
    template_name = 'My_App/comment.html'

    def get_success_url(self):
            return reverse('dashboard')


def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/dashboard')
    elif request.user.is_authenticated:
        return redirect('/dashboard2')
    else:

        return render(request,'My_App/home.html')


@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url']  and request.FILES['image']:
            prod = ImageUpload()
            prod.title = request.POST['title']
            prod.body = request.POST['body']
            if request.POST['url'].startswith("http://") or request.POST['url'].startswith("https://"):
                prod.url = request.POST['url']
            else:
                prod.url = 'http://'+ request.POST['url']
            prod.image = request.FILES['image']
            prod.pub_date = timezone.datetime.now()
            prod.email = request.user
            prod.save()
            return redirect('/dashboard2')

        else:
            return render(request,'My_App/create.html',{'error':'all fields are require'})





    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/dashboard')
    elif request.user.is_authenticated:

        return render(request,'My_App/create.html')
    else:
        return redirect('/login')


#testing ip to location flag.
import geoip2.database
reader = geoip2.database.Reader('./GeoLite2-Country_20190521/GeoLite2-Country.mmdb')
try:
    response = reader.country('127.0.0.1')
except:
    response = "India"
    print(response)
reader.close()

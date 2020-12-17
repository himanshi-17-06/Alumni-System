'''from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.decorators.cache import cache_control
from .decorators import unauthenticated_user, allowed_users


@unauthenticated_user
def home(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name = 'alumni')
            user.groups.add(group)
            messages.success(request, "account was created for "+ username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'data/signup.html', context)
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    return render(request, 'data/login.html')
def logoutUser(request):
    logout(request)
    return redirect('login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    return render(request, 'data/user_dashboard.html')
#def signup(request):
#   return render(request, 'data/signup.html')
# Create your views here.
'''
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse 
from django.urls import reverse
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView
from .forms import CreateUserForm, AlumniForm, NoticeForm, ComposeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.views.decorators.cache import cache_control
from .decorators import unauthenticated_user, allowed_users
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import *
from .filters import AlumniFilter
from braces.views import LoginRequiredMixin
from django.views import generic
from django.contrib.auth import get_user_model

class UserListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'data/users.html'
    login_url = 'admin/'

def home(request):
    return render(request, 'data/home.html')
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name = 'alumni')
            user.groups.add(group)
            Alumni.objects.create(
                user = user,
                email = user.email,
                name = user.username,
                )
                      
            current_site = get_current_site(request)
            mail_subject = 'Activate Your account'
            message = render_to_string('data/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
         #   username = form.cleaned_data.get('username')
         #   group = Group.objects.get(name = 'alumni')
         #  user.groups.add(group)
         #   messages.success(request, "account was created for "+ username)
         #  return redirect('login')
    context = {'form':form}
    return render(request, 'data/signup.html', context)
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    return render(request, 'data/login.html')
@unauthenticated_user
def adminloginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    return render(request, 'data/login.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@allowed_users(allowed_roles=['alumni'])
def userProfile(request):
    alumni = request.user.alumni
    form = AlumniForm(instance= alumni)

    if request.method=='POST':
        form = AlumniForm(request.POST, request.FILES, instance= alumni)
        if form.is_valid():
            form.save()
    context={'form': form}
    return render(request, 'data/user_profile.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    notices = Notice.objects.all()
    context = {'notices': notices}
    return render(request, 'data/user_dashboard.html', context)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def admin_dashboard(request):
    #alumni = User.objects.all()
    alumni = User.objects.filter(groups__name='alumni')
    myFilter = AlumniFilter(request.GET, queryset=alumni)
    alumni = myFilter.qs
    context = {'alumni': alumni, 'myFilter': myFilter}
    return render(request, 'data/admin_dashboard.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def admin_view_profile(request, pk):
    alumni = User.objects.get(id = pk)
    profile = Alumni.objects.get(user = alumni)
    context = {'alumni':alumni, 'profile':profile}
    return render(request, 'data/alumni_view_profile.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def delete_alumni(request, pk):
    alumni = User.objects.get(id = pk)
    if request.method == "POST":
        alumni.delete()
        return redirect('admin_dashboard')

    context={'alumni':alumni}
    return render(request, 'data/delete_alumni.html',context)

def delete_file(request, pk):
    notices = Notice.objects.get(id = pk)
    if request.method == 'POST':
        notices.delete()
        return redirect('notices_list')
    context = {'item':notices}
    return render(request, 'data/delete_file.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def notices_list(request, pk):
    alumni = User.objects.get(id = pk)
    notices = alumni.notice_set.all()
    return render(request, 'data/notices_list.html',{
        'notices':notices
    })
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def notices_list_admin(request, pk):
    alumni = User.objects.get(id = pk)
    notices = alumni.notice_set.all()
    return render(request, 'data/notices_list_admin.html',{
        'notices':notices
    })
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def upload_notices(request, pk):
    alumnii = User.objects.get(id = pk)
    form = NoticeForm()
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance = Notice.objects.create(alumni = alumnii,))
        
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'data/upload_notices.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def upload_notices_admin(request, pk):
    alumnii = User.objects.get(id = pk)
    form = NoticeForm()
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance = Notice.objects.create(alumni = alumnii,))
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'data/upload_notices_admin.html', context)
def logoutUser(request):
    logout(request)
    return redirect('login')
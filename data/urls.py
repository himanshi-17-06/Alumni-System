from __future__ import absolute_import, unicode_literals


from django.urls import path

#from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url
urlpatterns = [
	url(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='user_list'
    ),
    path('home/', views.home, name = 'home'),
    path('register',views.register, name='register'),
    path('login/', views.loginPage, name='login'),
	path('adminlogin/', views.adminloginPage, name='adminlogin'),
    path('logout/', views.logoutUser, name='logout'),
    path('user_dashboard/', views.dashboard, name= 'dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name= 'admin_dashboard'),
    path('admin_view_profile/<str:pk>/', views.admin_view_profile, name='admin_view_profile'),
    path('delete_alumni/<str:pk>/', views.delete_alumni, name='delete_alumni'),
    path('delete_file/<str:pk>/', views.delete_file, name='delete_file'),
    path('upload_notices/<str:pk>/', views.upload_notices, name= 'upload_notices'),
    path('upload_notices_admin/<str:pk>/', views.upload_notices_admin, name= 'upload_notices_admin'),
    path('notices_list/<str:pk>/', views.notices_list, name= 'notices_list'),
    path('notices_list_admin/<str:pk>/', views.notices_list_admin, name= 'notices_list_admin'),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate, name='activate'),
    path('user_profile/',views.userProfile, name='user_profile'),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name = "data/password_reset.html"), name="reset_password"),
    path('reset_password_sent/',
     auth_views.PasswordResetDoneView.as_view(template_name = "data/password_reset_sent.html"), name = "password_reset_done"),
    path('reset_password/<uidb64>/<token>/',
    	auth_views.PasswordResetConfirmView.as_view(template_name="data/password_reset_form.html"), name ="password_reset_confirm"),
    path('reset_password_complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name = "data/password_reset_done.html"), name = "password_reset_complete"),

 #   path('signup.html/', views.signup, name = 'signup'),
]#+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

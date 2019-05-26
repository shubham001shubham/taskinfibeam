from django.urls import path,include
from .views import home
from .views import register, logout, login, dashboard , dashboard2, create, userimage, UpdateComment#, test #userimagecommnet#, LoginView


urlpatterns = [
    path('acc/',register,name='register'),
    path('acc/out/',logout,name='logout'),
    path('login/', login, name='login'),
    path('',home,name='home'),
    path('dashboard',dashboard,name='dashboard'),
    path('dashboard2',dashboard2,name='dashboard2'),
    path('crt/',create,name='create'),
    path('user/<id>/',userimage,name='userprofile'),
    path('user/img/<pk>/',UpdateComment.as_view(),name='commment'),

    #path('test',test)


]

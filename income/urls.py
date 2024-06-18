"""income URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from regin.views import index,home,single,contact,about,filter_data,search,Coursedetail,pagenot,checkout,Mycourse
from regin import user_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
     path('home/', index),
     path('',home,name='home'),
     path('course/<slug:slug>',Coursedetail,name = 'coursedetail'),
       path('Courses/',single,name='single'),
        path('about/',about,name='about'),
        path('contact/',contact,name='contact'),
         path('accounts/register',user_login.REGISTER,name='register'),
        path('accounts/', include('django.contrib.auth.urls'),name='login'),
        path('search',search,name='search'),
          path('404',pagenot,name='404'),
      
path('course/filter-data',filter_data,name="filter-data"),


          path('Dologin/', user_login.DOLOGIN,name='Dologin'),
             path('mycourse',Mycourse,name='mycourse'),
          path('accounts/profile',user_login.PROFILE,name='profile'),
           path('accounts/profile/update',user_login.Profile_Update,name='profileupdate'),
           path('checkout/<slug:slug>',checkout,name='checkout'),
] + static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)

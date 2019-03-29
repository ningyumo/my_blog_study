"""myboke URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('login_for_modal/', views.login_for_modal, name='login_for_modal'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('blog/', include('blog.urls',namespace='blog')),
    path('comment/', include('comment.urls', namespace='comment')),
    path('like/', include('like.urls', namespace='like')),
    path('user_info/<int:user_pk>/', views.user_info, name='user_info'),
    path('change_nick_name/', views.change_nick_name, name='change_nick_name'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_verify_code/', views.send_verify_code, name='send_verify_code'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
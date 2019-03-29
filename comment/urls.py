from django.urls import path
from . import views


app_name = 'comment'
urlpatterns = [
    path('submit/', views.submit_comment, name='submit_comment'),
]
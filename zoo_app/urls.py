from django.urls import path
from . import views

urlpatterns = [
    path('', views.classify, name='classify'),
    path('history_nan', views.history, name='history_nan'),
    path('history', views.history, name='history'),
    path('signup', views.signup, name='signup'),
]

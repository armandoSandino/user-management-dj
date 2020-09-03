from django.urls import path, re_path, include
# Views
from . import views

app_name = 'home_app'

urlpatterns = [
    path('home/', views.HomePage.as_view(), name ='your-house'),
    path('mixin/', views.TemplatePruebaMixin.as_view(), name='mixin')
]
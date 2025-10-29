from django.urls import path
from . import views

app_name = 'metrics'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('data/', views.data_view, name='data'),
    path('reports/', views.reports_view, name='reports'),
    path('technical/', views.technical_notes, name='technical'),
    
    
]
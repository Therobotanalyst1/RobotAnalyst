from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('betaCalc', views.betaCalc, name='betaCalc'),
    path('peCalc', views.peCalc, name='peCalc'),
    path('avgGrowth', views.avgGrowth, name='avgGrowth'),
    path('years', views.years, name='years'),
    path('revenueCalc', views.revenueCalc, name='revenueCalc')
]
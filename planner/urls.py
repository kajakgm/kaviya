from django.urls import path
from . import views  # Import views from planner app

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-room/', views.add_room, name='add_room'),
    path('view-plan/<int:plan_id>/', views.view_plan, name='view_plan'),
    path('register/', views.register, name='register'),
    path("generate_2d_plan/",views.generate_2d_plan, name="generate_2d_plan"),
    #path('generate-plan/', views.generate_2d_plan, name='generate_2d_plan'),
]

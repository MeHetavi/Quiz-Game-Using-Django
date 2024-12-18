from django.contrib import admin
from django.urls import path
from quiz import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup',views.signUp,name='signup'),
    path('login',views.login,name='login'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('home',views.home,name='home'),
    path('quiz/<str:genre>/', views.quiz, name='quiz'),
    path('logout',views.logout_view,name='logout'),
]
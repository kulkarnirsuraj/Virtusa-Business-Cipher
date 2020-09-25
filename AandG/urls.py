from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from AandG import views

app_name='my_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login_page, name='login'),
    path('home/', views.index, name='index'),
    path('logout/',views.logout_page,name='logout'),
    path('Aform/', views.index1, name='Aform'),
    path('output/', views.index2, name='output'),
    path('Aformsample1/',views.index3, name='AformA'),
    path('Aformsample2/',views.index4, name='AformA2'),
    path('Aformsample3/',views.index5, name='AformD'),
    path('Aformsample4/',views.index6, name='AformD2'),
    path('dashboard/',views.dashboard,name='dashboard'),
]

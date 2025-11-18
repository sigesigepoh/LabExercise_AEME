from django.contrib import admin
from django.urls import path
from salesapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name="homepage"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('about/', views.about_page, name="about"),
    path('contact/', views.contact_page, name="contact"),
]

from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup_user, name="signup"),
    path('login', views.login_user, name="login"),
    path('login/<int:task_id>', views.delete, name="delete"),
    path('add', views.add, name="add"),
    path('', views.logout_user, name="logout"),
]

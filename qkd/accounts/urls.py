from django.conf.urls import url
from django.urls import path,include
from .views import registerview
from .views import loginview,logoutview,chat,reviews
app_name='accounts'

urlpatterns = [
    path(r'register/', registerview, name="register"),
    path(r'login/', loginview, name="login"),
    path(r'logout/', logoutview, name="logout"),
    path(r'<s_idx>/<r_idx>/chat/', chat, name="chat"),
    path(r'<id>/<idx>/<add>/reviews/', reviews, name="reviews"),
   


]
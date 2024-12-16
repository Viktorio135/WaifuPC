from django.urls import include, path
from .views import Logout

from .views import *

app_name = 'main'


urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path("logout/", Logout.as_view(), name="logout"),
    path('registration/', RegisterPage.as_view(), name='register'),
    path('profile/', ProfilePage.as_view(), name='profile'),
]

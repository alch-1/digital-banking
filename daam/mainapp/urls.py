from django.urls import path,include
from . import views
from .views import login_view, signup_view, homepage_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns = [
    path('',homepage_view, name='homepage'),
    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

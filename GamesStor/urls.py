"""
URL configuration for GamesStor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("main/", views.main, name="main"),
    path("", views.home, name="home"),
    path("items_list/", views.items_list, name="items_list"),
    path("product_card/<int:game_id>/", views.product_card, name="product_card"),
    path("shopping_cart/", views.shopping_cart, name="shopping_cart"),
    path("profile/", views.profile, name="profile"),
    path("accounts/login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("accounts/logout/", LogoutView.as_view(next_page="logout_now"), name="logout"),
    path("logout_now/", views.logout_account, name="logout_now"),
    path("register/", views.register, name='register'),
    path("add_to_cart/<int:game_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<int:game_id>/", views.remove_from_cart, name="remove_from_cart"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
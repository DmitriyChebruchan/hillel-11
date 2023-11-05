from django.contrib import admin
from django.urls import path, include

from exchange.views import main_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("exchange-rates", main_view),
    path("/", include('exchange.urls'))]

from django.urls import path, include
from .views import laylo_view


urlpatterns = [
    path("laylo", include(laylo_view))
]

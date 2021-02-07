from django.urls import path, include


urlpatterns = [
     path("s/", include('s.urls')),
]

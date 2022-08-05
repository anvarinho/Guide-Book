from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('places/', views.getRooms),
    path('tours/', views.getTours),
    path('places/<str:pk>', views.getRoom),
    path('tours/<str:pk>', views.getTour),
]

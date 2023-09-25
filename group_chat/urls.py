from django.urls import path

from . import views
from rest_framework import routers

route = routers.SimpleRouter(trailing_slash=False)
route.register(r'groups',views.GroupViewSet,basename='group')



urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]

urlpatterns += route.urls
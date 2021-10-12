from django.urls import path
from .views import ListPersons

urlpatterns = [
    path("",ListPersons.as_view()),
    path(r"<int:id>", ListPersons.as_view()),
]

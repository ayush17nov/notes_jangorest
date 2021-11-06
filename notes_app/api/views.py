from django.http import request, HttpResponse
from django.shortcuts import render
from rest_framework import generics

from .models import Note
from .serializers import NoteSerializer


# defining views
def home(request):
    return render(request, "home.html", context={})

class NoteList(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

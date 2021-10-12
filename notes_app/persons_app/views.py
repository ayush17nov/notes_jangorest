# Ayush G copyright@2021

from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Person
from .serializers import PersonSerializer


class ListPersons(APIView):
    """A simple class has http methods view like get post put patch delete.
    used class based approach with APIView class to develop rest method implementation for Person app.
    """
    def get_object(self, id):
        """returns mdoel object by its id but raise Http404 error if object not exists"""
        try:
            return Person.objects.get(id=id)
        except Person.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        """This method lists all available persons and its detail"""
        persons = Person.objects.all()
        if persons:
            serializer = PersonSerializer(persons, many=True)
            p_list = serializer.data
            return Response(p_list, status.HTTP_200_OK)
        return Response({"message": "data not found"}, status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Add new person detail but email id has unique constraint so two person cannot have same email id"""
        try:
            serializer = PersonSerializer(data=request.data)
            eml = Person.objects.get(email=request.data['email'])
            print(eml)
        except Person.DoesNotExist:
            pass
        except:
            return Response({"message": "Request data format might be wrong."}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "email id already exists"}, status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Person added sucessfully."}, status.HTTP_201_CREATED)
        return Response({"message": serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        """update person detail but all fields are required by this method to update person detail"""
        person = self.get_object(id)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Person updated sucessfully."}, status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        """Update person detail but this method allows partial update, so the provided field's data would be updated only"""
        person = self.get_object(id)
        serializer = PersonSerializer(person, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Person updated sucessfully."}, status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        """Deletes the object requested by its id"""
        person = self.get_object(id)
        person.delete()
        return Response({"message": "Person deleted successfully."}, status.HTTP_204_NO_CONTENT)

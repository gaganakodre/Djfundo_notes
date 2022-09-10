from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from notes.models import Notes
from notes.serializers import NoteSerializer


# Create your views here.
class Note(APIView):
    """
    This class performs CRUD operation for Notes model
    """

    def post(self, request):
        """
        This method create note for user
        """
        try:
            print(request.data)
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Note Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"message": ex.detail, "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        This method used to retrieve the data
        """

        try:
            notes = Notes.objects.filter(user=request.data.get('user'))
            serializer = NoteSerializer(notes, many=True)
            return Response({"message": "Data Retrieved", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        This method update the note of a user
        """
        try:
            note=Notes.objects.get(id=request.data.get("id"))
            serializer = NoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Note Updated", "status": 201, "data": serializer.data},
                            status=status.HTTP_202_ACCEPTED)
        except ValidationError as e:
            return Response({"message": str(e), "status": 406, "data": {}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        This method delete the note of a user
        """
        try:
            note_object = Notes.objects.get(id=request.data.get('id'))
            note_object.delete()
            return Response({"message": "Note Deleted", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

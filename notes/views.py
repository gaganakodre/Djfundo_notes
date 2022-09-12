from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from notes.models import Notes
from notes.serializers import NoteSerializer
import logging

logging.basicConfig(filename='Djfundo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


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
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info("notes created successfully")
            return Response({"message": "Note Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            logger.error(ex)
            return Response({"message": ex.detail, "status": 403, "data": {}}, status=status.HTTP_403_FORBIDDEN)
        except Exception as ex:
            logger.error(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        This method used to retrieve the data
        """

        try:
            notes = Notes.objects.filter(user=request.data.get('user'))
            serializer = NoteSerializer(notes, many=True)
            logger.info("Retrieved data successfully")
            return Response({"message": "Data Retrieved", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
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
            logger.info(" data updated successfully")
            return Response({"message": "Note Updated", "data": serializer.data},
                            status=status.HTTP_202_ACCEPTED)
        except ValidationError as e:
            logger.error(e)
            return Response({"message": str(e), "status": 406, "data": {}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            logger.error(e)
            return Response({"message": str(e), "status": 404, "data": {}}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        """
        This method delete the note of a user
        """
        try:
            note_object = Notes.objects.get(id=request.data.get('id'))
            note_object.delete()
            logger.info(" data deleted successfully")
            return Response({"message": "Note Deleted", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"message": str(e), "status": 404, "data": {}},
                        status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

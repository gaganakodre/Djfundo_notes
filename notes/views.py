import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from notes.models import Notes
from notes.serializers import NoteSerializer
from user.models import User
from user.token import verify_token

logging.basicConfig(filename='Djfundo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


# Create your views here.
class Note(APIView):
    """
    This class performs CRUD operation for Notes model
    """

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={
                                                         'title': openapi.Schema(type=openapi.TYPE_STRING),
                                                         'description': openapi.Schema(
                                                             type=openapi.TYPE_STRING),
                                                     },
                                                     required=['title', 'description']),
                         operation_summary='create Notes')
    @verify_token
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

    @verify_token
    def get(self, request):
        """
        This method used to retrieve the data
        """

        try:
            # notes = Notes.objects.filter(user_id=user_id, is_deleted=False, is_archived=False)
            # notes = Notes.objects.filter(user=request.data.get('user'), is_pinned=True, is_archive=False)
            notes = Notes.objects.filter(user=request.data.get('user')).order_by("-is_pinned")
            serializer = NoteSerializer(notes, many=True)
            logger.info("Retrieved data successfully")
            return Response({"message": "Data Retrieved", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 'title': openapi.Schema(type=openapi.TYPE_STRING),
                                                                 'description': openapi.Schema(
                                                                     type=openapi.TYPE_STRING),
                                                                 },
                                                     required=['id', 'title', 'description']),
                         operation_summary='Update Notes')
    @verify_token
    def put(self, request):
        """
        This method update the note of a user
        """
        try:

            note = Notes.objects.get(id=request.data.get('id'))
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

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={
                                                         'id': openapi.Schema(type=openapi.TYPE_STRING),
                                                     },
                                                     required=['id']),
                         operation_summary='delete Notes')
    @verify_token
    def delete(self, request):
        """
        This method delete the note of a user
        """
        try:
            note_object = Notes.objects.filter(id=request.data.get('id'))
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


class Collaborator(APIView):

    @verify_token
    def put(self, request):
        """
        Add a new note
        """
        try:
            collabrator = request.data.get("collabrator")
            note = Notes.objects.get(id=request.data.get("id"))
            if request.data.get("user") in collabrator:
                raise Exception("auth user  cannot be part of collabrator")
            note.collaborator.set(collabrator)
            note.save()
            serializer = NoteSerializer(note)
            return Response({
                "message": "user found", "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        try:
            user = User.objects.get(id=request.data.get('collabrator'))
            note = Notes.objects.get(id=request.data.get('id'))
            print(note)
            note.collaborator.clear()
            return Response({"message": "Collaborator Removed", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class PinnedNotes(APIView):
    def put(self, request, *args, **kwargs):
        try:
            id = self.kwargs.get("id")
            note_id = id
            note = Notes.objects.get(id=note_id)
            if not note.is_pinned:
                note.is_pinned = True
                note.save()
                return Response({"data": "is pinned"}, status=status.HTTP_200_OK)
            elif note.is_pinned:
                note.is_pinned = False
                note.save()
                return Response({"data": "is unpinned"}, status=status.HTTP_200_OK)



        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class Archive(APIView):

    def put(self, request, *args, **kwargs):
        """
        This method update the note of a user
        """
        try:

            id = self.kwargs.get("id")
            note_id = id
            note = Notes.objects.get(id=note_id)
            if not note.is_archive:
                note.is_archive = False
                note.save()
                return Response({"data": "note archived"}, status=status.HTTP_200_OK)
            elif note.is_archive:
                note.is_archive = True
                note.save()
            logger.info(" data updated successfully")
            return Response({"message": "notes not archived"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({"message": str(e), "status": 404, "data": {}}, status=status.HTTP_404_NOT_FOUND)


class AddLabelToNote(APIView):
    @verify_token
    def put(self, request):
        """
        Add a new note
        """
        try:
            labels = request.data.get("labels")
            note = Notes.objects.get(id=request.data.get("id"))
            note.labels.set(labels)
            note.save()
            serializer = NoteSerializer(note)
            return Response({
                "message": "user found", "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        try:
            user = User.objects.get(id=request.data.get('labels'))
            note = Notes.objects.get(id=request.data.get('id'))
            note.labels.clear()
            return Response({"message": "label Removed", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

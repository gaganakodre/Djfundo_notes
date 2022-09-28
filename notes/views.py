from django.db import connection
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
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
            note = Notes.objects.get(id=request.data.get("id"))
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


class RawQueriesNotes(APIView):
    def post(self, request):
        user=request.data.get("user")
        title= request.data.get("title")
        description=request.data.get("description")
        is_pinned=request.data.get("is_pinned")
        is_archive = request.data.get("is_archive")

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO notes_notes(title,description,user_id,is_pinned, is_archive) VALUES (%s, %s, %s,%s, %s)",
                (title, description, user, is_pinned, is_archive)
            )
            cursor.execute("select * from notes_notes where user_id='%s'" % (user))
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return Response({"message": "data Created", "status": 201,"data":data},
                            status=status.HTTP_201_CREATED)

    def get(self, request):
        
        notes = Notes.objects.raw('select * from notes_notes where user_id = %s', [request.data.get("user")])
        # data = [{"id": x.id, "title": x.title, "description": x.description,  "user": x.user_id} for x in notes]
        data = [model_to_dict(x,["id","title","description","user"]) for x in notes]

        return Response({"message": "Data Retrieved", "status": 200, "data": data},
                        status=status.HTTP_200_OK)
    def put(self, request):    
        with connection.cursor() as cursor:
            # cursor.execute('update notes_notes set title = %(title)s, description = %(discription)s where id = %(id)s and user_id = %(user)s',
            #                 [request.data.get('title'), request.data.get('description'),
            #                 request.data.get('id'), request.data.get('user')])
            cursor.execute(
                'update notes_notes set title = %(title)s, description = %(description)s where id = %(id)s and user_id = %(user)s',
                request.data)
            cursor.execute('select * from notes_notes where id = %s', [request.data.get('id')])
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response({"message": "Note Updated", "status": 202, "data": data[0]},
                        status=status.HTTP_202_ACCEPTED)
    def delete(self, request):
        with connection.cursor() as cursor:
            cursor.execute('delete from notes_notes where user_id = %s and id = %s',
                            [request.data.get('user'), request.data.get('id')])
        return Response({"message": "Note Deleted", "status": 204, "data": {}},
                        status=status.HTTP_204_NO_CONTENT)
        

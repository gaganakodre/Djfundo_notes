from django.shortcuts import render

# Create your views here.
import logging
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from user.token import verify_token
from .serializers import LabelSerializer
from .models import Labels

logging.basicConfig(filename='Djfundo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


# Create your views here.
class Label(APIView):
    """
    This class performs CRUD operation for Labels model
    """
    @verify_token
    def post(self, request):
        """
        This method create labels for user
        """
        try:
            serializer = LabelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info("labels created successfully")
            return Response({"message": "labels Created", "status": 201, "data": serializer.data},
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
            label = Labels.objects.all()
            serializer = LabelSerializer(label, many=True)
            logger.info("Retrieved data successfully")
            return Response({"message": "Data Retrieved", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        """
        This method delete the labels of a user
        """
        try:
            note_object = Labels.objects.get(id=request.data.get('id'))
            note_object.delete()
            logger.info(" data deleted successfully")
            return Response({"message": "Label Deleted", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"message": str(e), "status": 404, "data": {}},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


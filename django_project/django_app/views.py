from rest_framework.views import APIView
from . import models
from . import serializers
import rest_framework.status as status
from rest_framework.response import Response

class MessageView(APIView):
  
  def get(self, request):
    messages = models.Messages.objects.all()
    serializer = serializers.MessageSerializer(messages, many=True)
    if not messages.exists():
      return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
    
from . import models
from rest_framework import serializers 


class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Messages
    fields = '__all__'
    

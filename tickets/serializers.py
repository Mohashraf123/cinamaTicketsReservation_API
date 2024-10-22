from rest_framework import serializers
from tickets.models import Guest,Movie,Reserevation


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields='__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reserevation
        fields='__all__'
        
class GuestSerializer(serializers.ModelSerializer):
    class Meta:   
        model=Guest
        fields=['pk','reservation','name','mobile']   
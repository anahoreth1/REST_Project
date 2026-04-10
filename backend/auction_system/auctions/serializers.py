from rest_framework import serializers
from .models import Auction


# Serializer zmienia model Auction na JSON i odwrotnie
class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        # Model, z którego korzysta serializer
        model = Auction
        
        # Wszystkie pola modelu mają być widpczne w API
        fields = "__all__"
        
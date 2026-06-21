from rest_framework import serializers

from .models import Auction, Bid


# Serializer zmienia model Auction na JSON i odwrotnie
class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        # Model, z którego korzysta serializer
        model = Auction

        # Wszystkie pola modelu mają być widoczne w API
        fields = "__all__"
        read_only_fields = ["current_price"]

    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError(
                "Data rozpoczęcia musi być wcześniejsza niż data zakończenia."
            )

        return data

    def create(self, validated_data):
        validated_data["current_price"] = validated_data["starting_price"]
        return Auction.objects.create(**validated_data)


class BidSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = ["id", "auction", "user", "user_name", "amount", "created_at"]
        read_only_fields = ["auction", "user", "user_name"]

    def get_user_name(self, obj):
        return getattr(obj.user, "name", None)

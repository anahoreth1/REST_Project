from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Auction
from .serializers import AuctionSerializer, BidSerializer


class AuctionListCreateView(generics.ListCreateAPIView):
    serializer_class = AuctionSerializer

    def get_queryset(self):
        queryset = Auction.objects.all()

        category = self.request.query_params.get("category")
        status_param = self.request.query_params.get("status")

        if category:
            queryset = queryset.filter(category=category)

        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset


class AuctionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer


class AuctionBiddingView(APIView):
    def post(self, request, auction_id):
        auction = get_object_or_404(Auction, id=auction_id)
        serializer = BidSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data["amount"]
        now = timezone.now()

        if auction.status == "ended":
            return Response(
                {"error": "Aukcja została zakończona."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if auction.status == "planned" or now < auction.start_date:
            return Response(
                {"error": "Nie można składać ofert przed rozpoczęciem aukcji."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amount < 0 or amount <= auction.current_price:
            return Response(
                {"error": "Oferta musi być większa od aktualnej ceny."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(auction=auction)
        auction.current_price = amount
        auction.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
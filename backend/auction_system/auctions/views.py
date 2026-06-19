from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Auction
from .serializers import AuctionSerializer, BidSerializer


# Widok do wyświetlania listy aukcji i dodawania nowych
class AuctionListCreateView(generics.ListCreateAPIView):
    serializer_class = AuctionSerializer

    def get_queryset(self):
        queryset = Auction.objects.all()

        # Aktualizacja statusów wszystkich aukcji
        for auction in queryset:
            old_status = auction.status
            auction.update_status()
            if old_status != auction.status:
                auction.save()

        # Pobranie parametrów filtrowania z adresu URL
        category = self.request.query_params.get("category")
        status_param = self.request.query_params.get("status")

        # Filtrowanie po kategorii
        if category:
            queryset = queryset.filter(category=category)

        # Filtrowanie po statusie
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset


# Widok do pobierania, edycji i usuwania jednej aukcji
class AuctionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

    def get_object(self):
        auction = super().get_object()
        old_status = auction.status
        auction.update_status()
        if old_status != auction.status:
            auction.save()
        return auction


# Widok do składania ofert
class AuctionBiddingView(APIView):
    def post(self, request, auction_id):
        auction = get_object_or_404(Auction, id=auction_id)

        # Aktualizacja statusu aukcji przed licytacją
        old_status = auction.status
        auction.update_status()
        if old_status != auction.status:
            auction.save()

        serializer = BidSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data["amount"]
        now = timezone.now()

        # Blokada ofert przed rozpoczęciem aukcji
        if now < auction.start_date or auction.status == "planned":
            return Response(
                {"error": "Nie można składać ofert przed rozpoczęciem aukcji."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Blokada ofert po zakończeniu aukcji
        if auction.status == "ended":
            return Response(
                {"error": "Aukcja została zakończona."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kwota musi być większa od aktualnej ceny
        if amount <= auction.current_price:
            return Response(
                {"error": "Oferta musi być większa od aktualnej ceny."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(auction=auction)
        auction.current_price = amount
        auction.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
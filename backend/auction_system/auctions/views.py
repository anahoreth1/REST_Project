from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

from .models import Auction, Bid
from .serializers import AuctionSerializer, BidSerializer

logger = logging.getLogger(__name__)


def update_auctions():
    logger.debug("update_auctions called")
    for auction in Auction.objects.all():
        auction.update_status()


class AuctionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuctionSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["start_date", "end_date", "current_price", "name"]
    ordering = ["start_date"]

    def get_queryset(self):
        update_auctions()

        queryset = Auction.objects.all()

        category = self.request.query_params.get("category")
        status_param = self.request.query_params.get("status")
        ordering = self.request.query_params.get("ordering")

        if category:
            queryset = queryset.filter(category=category)

        if status_param:
            queryset = queryset.filter(status=status_param)

        allowed_ordering_fields = [
            "name",
            "current_price",
            "start_date",
            "end_date",
            "status",
            "category",
        ]

        if ordering:
            ordering_field = ordering.lstrip("-")
            if ordering_field in allowed_ordering_fields:
                queryset = queryset.order_by(ordering)

        return queryset


class AuctionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuctionSerializer

    def get_queryset(self):
        update_auctions()

        queryset = Auction.objects.all()

        category = self.request.query_params.get("category")
        status_param = self.request.query_params.get("status")

        if category:
            queryset = queryset.filter(category=category)

        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset


# Widok do obsługi listowania i składania ofert
# (obsługa `GET /auctions/{id}/bids` i `POST /auctions/{id}/bids`)
class BidListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, auction_id):
        logger.info("Listing bids for auction %s", auction_id)
        auction = get_object_or_404(Auction, id=auction_id)

        bids = Bid.objects.filter(auction=auction).order_by("-created_at")

        serializer = BidSerializer(bids, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, auction_id):
        logger.info("Creating bid for auction %s by user %s", auction_id, request.user.id)
        auction = get_object_or_404(Auction, id=auction_id)

        auction.update_status()

        serializer = BidSerializer(data=request.data)

        if not serializer.is_valid():
            logger.warning("Bid validation failed for auction %s: %s", auction_id, serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data["amount"]

        # aukcja nie jest aktywna
        if auction.status != "active":
            logger.warning("Bid rejected because auction %s is not active", auction_id)
            return Response(
                {"detail": "Aukcja nie jest aktywna."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # oferta za niska
        if amount <= auction.current_price:
            logger.warning(
                "Bid rejected for auction %s: amount %s <= current_price %s",
                auction_id,
                amount,
                auction.current_price,
            )
            return Response(
                {"detail": "Oferta musi być wyższa niż aktualna cena."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bid = serializer.save(auction=auction, user=request.user)

        auction.current_price = amount
        auction.save(update_fields=["current_price"])

        logger.info("Bid created for auction %s by user %s: %s", auction_id, request.user.id, amount)
        return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)
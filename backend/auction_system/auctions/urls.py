from django.urls import path

from .views import AuctionDetailView, AuctionListCreateView, BidListCreateView

urlpatterns = [
    path("auctions/", AuctionListCreateView.as_view(), name="auction-list-create"),
    path("auctions/<int:pk>/", AuctionDetailView.as_view(), name="auction-detail"),
    path(
        "auctions/<int:auction_id>/bids/",
        BidListCreateView.as_view(),
        name="auction-bid",
    ),
]

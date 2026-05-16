from django.urls import path
from .views import AuctionListCreateView, AuctionDetailView, AuctionBiddingView

urlpatterns = [
    path("auctions/", AuctionListCreateView.as_view()),
    path("auctions/<int:pk>/", AuctionDetailView.as_view()),
    path("auctions/<int:auction_id>/bids", AuctionBiddingView.as_view())
]
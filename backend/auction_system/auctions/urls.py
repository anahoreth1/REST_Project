from django.urls import path
from .views import AuctionListCreateView, AuctionDetailView

urlpatterns = [
    path("auctions/", AuctionListCreateView.as_view(), name="auction-list-create"),
    path("auctions/<int:pk>/", AuctionDetailView.as_view(), name="auction-detail"),
]
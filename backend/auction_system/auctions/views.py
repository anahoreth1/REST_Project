from rest_framework import generics
from .models import Auction
from .serializers import AuctionSerializer

# Widok do wyświetlania listy aukcji i dodawanie nowych
class AuctionListCreateView(generics.ListCreateAPIView):
    serializer_class = AuctionSerializer
    
    def get_queryset(self):
        queryset = Auction.objects.all()
        
        #Pobranie parametrów filtrowania z adresu URL
        category = self.request.query_params.get("category")
        status_param = self.request.query_params.get("status")
        
        # Filtrowanie po kategorii
        if category:
            queryset = queryset.filter(category=category)
            
        # Filtrowanie po statusie
        if status_param:
            queryset = queryset.filter(status = status_param)
        
        
        return queryset
# Widok do pobierania, edycji i usuwania jednej aukcji
class AuctionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer


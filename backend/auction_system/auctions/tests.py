

from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .models import Auction


# Testy API dla obsługi aukcji
class AuctionApiTest(APITestCase):

    # Test tworzenia nowej aukcji
    def test_create_auction(self):
        data = {
            "name": "Laptop Dell",
            "description": "Używany laptop w dobrym stanie",
            "category": "elektronika",
            "starting_price": "1500.00",
            "current_price": "1500.00",
            "start_date": timezone.now().isoformat(),
            "end_date": (timezone.now() + timedelta(days=1)).isoformat(),
            "owner_id": 1,
            "status": "active"
        }

        response = self.client.post("/api/auctions/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test pobierania listy aukcji
    def test_get_auction_list(self):
        Auction.objects.create(
            name="Laptop Dell",
            description="Opis",
            category="elektronika",
            starting_price="1500.00",
            current_price="1500.00",
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=1,
            status="active"
        )

        response = self.client.get("/api/auctions/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Test pobierania jednej aukcji
    def test_get_single_auction(self):
        auction = Auction.objects.create(
            name="Laptop Dell",
            description="Opis",
            category="elektronika",
            starting_price="1500.00",
            current_price="1500.00",
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=1,
            status="active"
        )

        response = self.client.get(f"/api/auctions/{auction.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test edycji aukcji
    def test_update_auction(self):
        auction = Auction.objects.create(
            name="Laptop Dell",
            description="Opis",
            category="elektronika",
            starting_price="1500.00",
            current_price="1500.00",
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=1,
            status="active"
        )

        data = {
            "name": "Laptop Dell i5",
            "description": "Lepszy opis",
            "category": "elektronika",
            "starting_price": "1500.00",
            "current_price": "1700.00",
            "start_date": auction.start_date.isoformat(),
            "end_date": auction.end_date.isoformat(),
            "owner_id": 1,
            "status": "active"
        }

        response = self.client.put(f"/api/auctions/{auction.id}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test usuwania aukcji
    def test_delete_auction(self):
        auction = Auction.objects.create(
            name="Laptop Dell",
            description="Opis",
            category="elektronika",
            starting_price="1500.00",
            current_price="1500.00",
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=1,
            status="active"
        )

        response = self.client.delete(f"/api/auctions/{auction.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test filtrowania aukcji po statusie
    def test_filter_auctions_by_status(self):
        Auction.objects.create(
            name="Laptop Dell",
            description="Opis",
            category="elektronika",
            starting_price="1500.00",
            current_price="1500.00",
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=1,
            status="active"
        )

        Auction.objects.create(
            name="Telefon",
            description="Opis",
            category="elektronika",
            starting_price="800.00",
            current_price="800.00",
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=2,
            status="ended"
        )

        response = self.client.get("/api/auctions/?status=active")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

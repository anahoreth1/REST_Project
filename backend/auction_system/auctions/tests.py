from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Auction, Bid

from users.models import User

# Testy API dla obsługi aukcji
class AuctionApiTest(APITestCase):
    # Przygotowanie przykładowej aukcji
    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com",
            name="Test User",
            password=make_password("password123"),
        )

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.auction = Auction.objects.create(
            name="testname",
            description="testdescription",
            category="testcategory",
            starting_price="100.00",
            current_price="100.00",
            start_date=timezone.now() - timedelta(days=3),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=1,
            status="active",
        )
        
    def test_get_auction_list_without_token(self):
        self.client.credentials()

        response = self.client.get("/api/auctions/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_auction_without_token(self):
        self.client.credentials()
        response = self.client.get(f"/api/auctions/{self.auction.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test tworzenia nowej aukcji
    def test_create_auction(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        data = {
            "name": "newauction",
            "description": "newdescription",
            "category": "newcategory",
            "starting_price": "200.00",
            "start_date": (timezone.now() - timedelta(days=3)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=2)).isoformat(),
            "owner_id": 1,
            "status": "active",
        }

        response = self.client.post("/api/auctions/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Auction.objects.filter(name="newauction").exists())

    # Test pobierania listy aukcji
    def test_get_auction_list(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        response = self.client.get("/api/auctions/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_auction_list_sorted_by_start_date(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        Auction.objects.create(
            name="earlyauction",
            description="early description",
            category="testcategory",
            starting_price="50.00",
            current_price="50.00",
            start_date=timezone.now() - timedelta(days=10),
            end_date=timezone.now() - timedelta(days=5),
            owner_id=2,
            status="ended",
        )

        Auction.objects.create(
            name="laterauction",
            description="later description",
            category="testcategory",
            starting_price="150.00",
            current_price="150.00",
            start_date=timezone.now() + timedelta(days=5),
            end_date=timezone.now() + timedelta(days=10),
            owner_id=3,
            status="planned",
        )

        response = self.client.get("/api/auctions/?ordering=start_date")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [auction["name"] for auction in response.data],
            ["earlyauction", "testname", "laterauction"],
        )

    def test_get_auction_list_sorted_by_end_date_desc(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        Auction.objects.create(
            name="soonerauction",
            description="soon end",
            category="testcategory",
            starting_price="80.00",
            current_price="80.00",
            start_date=timezone.now() - timedelta(days=5),
            end_date=timezone.now() + timedelta(hours=12),
            owner_id=2,
            status="active",
        )

        Auction.objects.create(
            name="laterauction",
            description="later end",
            category="testcategory",
            starting_price="120.00",
            current_price="120.00",
            start_date=timezone.now() - timedelta(days=2),
            end_date=timezone.now() + timedelta(days=10),
            owner_id=3,
            status="active",
        )

        response = self.client.get("/api/auctions/?ordering=-end_date")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [auction["name"] for auction in response.data],
            ["laterauction", "testname", "soonerauction"],
        )

    def test_get_auction_list_sorted_by_start_date_desc(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        Auction.objects.create(
            name="oldauction",
            description="old start",
            category="testcategory",
            starting_price="70.00",
            current_price="70.00",
            start_date=timezone.now() - timedelta(days=10),
            end_date=timezone.now() - timedelta(days=5),
            owner_id=2,
            status="ended",
        )

        Auction.objects.create(
            name="newauction",
            description="new start",
            category="testcategory",
            starting_price="180.00",
            current_price="180.00",
            start_date=timezone.now() + timedelta(days=5),
            end_date=timezone.now() + timedelta(days=6),
            owner_id=3,
            status="planned",
        )

        response = self.client.get("/api/auctions/?ordering=-start_date")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [auction["name"] for auction in response.data],
            ["newauction", "testname", "oldauction"],
        )

    def test_get_auction_list_sorted_by_current_price_asc(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        Auction.objects.create(
            name="cheapauction",
            description="cheap",
            category="testcategory",
            starting_price="10.00",
            current_price="10.00",
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=2,
            status="active",
        )

        Auction.objects.create(
            name="expensiveauction",
            description="expensive",
            category="testcategory",
            starting_price="300.00",
            current_price="300.00",
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=3,
            status="active",
        )

        response = self.client.get("/api/auctions/?ordering=current_price")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [auction["name"] for auction in response.data],
            ["cheapauction", "testname", "expensiveauction"],
        )

    def test_get_auction_list_sorted_by_name_desc(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        Auction.objects.create(
            name="alphaauction",
            description="alpha",
            category="testcategory",
            starting_price="20.00",
            current_price="20.00",
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=2,
            status="active",
        )

        Auction.objects.create(
            name="zuluauction",
            description="zulu",
            category="testcategory",
            starting_price="40.00",
            current_price="40.00",
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=3,
            status="active",
        )

        response = self.client.get("/api/auctions/?ordering=-name")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [auction["name"] for auction in response.data],
            ["zuluauction", "testname", "alphaauction"],
        )

    # Test pobierania jednej aukcji
    def test_get_single_auction(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        response = self.client.get(f"/api/auctions/{self.auction.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test pobierania aukcji po id
    def test_get_auction_by_id(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        response = self.client.get(f"/api/auctions/{self.auction.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["name"], "testname")

    # Test edycji aukcji
    def test_update_auction(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        data = {
            "name": "newauction",
            "description": "newdescription",
            "category": "newcategory",
            "starting_price": "150.00",
            "start_date": (timezone.now() - timedelta(days=1)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=3)).isoformat(),
            "owner_id": 1,
            "status": "active",
        }

        response = self.client.put(
            f"/api/auctions/{self.auction.id}/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.auction.refresh_from_db()

        self.assertEqual(self.auction.name, "newauction")
        self.assertEqual(self.auction.description, "newdescription")
        self.assertEqual(self.auction.category, "newcategory")

    # Test usuwania aukcji
    def test_delete_auction(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        response = self.client.delete(f"/api/auctions/{self.auction.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        exists = Auction.objects.filter(id=self.auction.id).exists()

        self.assertEqual(exists, False)

    # Test filtrowania aukcji po statusie
    def test_filter_auctions_by_status(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        Auction.objects.create(
            name="Telefon",
            description="Opis",
            category="elektronika",
            starting_price="800.00",
            current_price="800.00",
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=2,
            status="ended",
        )

        response = self.client.get("/api/auctions/?status=active")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class BiddingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com",
            name="Test User",
            password=make_password("password123"),
        )

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.auction = Auction.objects.create(
            name="testname",
            description="testdescription",
            category="testcategory",
            starting_price="100.00",
            current_price="100.00",
            start_date=timezone.now() - timedelta(days=3),
            end_date=timezone.now() + timedelta(days=1),
            owner_id=1,
            status="active",
        )

    def test_create_bid_without_token(self):
        self.client.credentials()
        data = {"amount": "150.00"}

        response = self.client.post(
            f"/api/auctions/{self.auction.id}/bids/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_bid(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        data = {"amount": "150.00"}

        response = self.client.post(
            f"/api/auctions/{self.auction.id}/bids/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        bid = Bid.objects.get(auction=self.auction, amount="150.00")
        self.assertEqual(bid.user, self.user)
        self.assertEqual(response.data.get("user"), self.user.id)
        self.assertEqual(response.data.get("user_name"), self.user.name)

    def test_wrong_amount_format(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        data = {"amount": "abcd"}

        response = self.client.post(
            f"/api/auctions/{self.auction.id}/bids/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bid_must_be_higher_than_current_price(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        data = {"amount": "90.00"}

        response = self.client.post(
            f"/api/auctions/{self.auction.id}/bids/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bid_updates_current_price(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        data = {"amount": "180.00"}

        response = self.client.post(
            f"/api/auctions/{self.auction.id}/bids/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.auction.refresh_from_db()

        self.assertEqual(str(self.auction.current_price), "180.00")

    def test_cannot_bid_on_ended_auction(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.auction.end_date = timezone.now() - timedelta(hours=3)
        self.auction.save()

        data = {"amount": "150.00"}

        response = self.client.post(
            f"/api/auctions/{self.auction.id}/bids/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

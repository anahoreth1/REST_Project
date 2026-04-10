from django.db import models

class Auction(models.Model):
    # Dostępne statusy aukcji
    STATUS_CHOICES = [
        ("active", "Active"),
        ("ended", "Ended")
    ]
    
    # Nazwa przedmiotu
    name = models.CharField(max_length=255)
    
    # Opis aukcji
    description = models.TextField()
    
    # Kategoria 
    category = models.CharField(max_length=100)
    
    # Cena Wywoławcza
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Aktualna najwyższa cena
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Data rozpoczęcia
    start_date = models.DateTimeField()
    
    # Data zakończenia
    end_date = models.DateTimeField()
    
    # Id właściciela
    owner_id = models.IntegerField()
    
    # Status aukcji
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    
    def __str__(self):
        return self.name
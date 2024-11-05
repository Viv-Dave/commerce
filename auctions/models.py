from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_name = models.BigAutoField(primary_key=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_name})"

class Listing(models.Model):
    listing_id = models.BigAutoField(primary_key=True)
    auction_item = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.IntegerField()
    updated_price = models.IntegerField()
    category = models.CharField(max_length=64)
    def __str__(self):
        return f"ID: {self.listing_id} Item: {self.auction_item} Category: {Listing.category}"

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
    product_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="auction_id")
    comment = models.TextField(max_length=200)

    def __str__(self):
        return f"On Product ID {self.product_id} User {self.username} comments {self.comment}"
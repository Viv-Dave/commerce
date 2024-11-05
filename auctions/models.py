from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
class User(AbstractUser):
    user_name = models.BigAutoField(primary_key=True)

    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    listing_id = models.BigAutoField(primary_key=True)
    auction_item = models.CharField(max_length=64)
    price = models.IntegerField()
    updated_price = models.IntegerField()
    category = models.CharField(max_length=64, default="General")
    active_status = models.BooleanField(default=True)
    def __str__(self):
        return f"ID: {self.listing_id} Item: {self.auction_item} Category: {self.category}"
class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    product_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentator")
    bid_price = models.IntegerField()

    def is_active(self):
        if not self.product_id.active_status:
            raise ValidationError("Can only place a bid if the listing is active.")
        return True 
    def __str__(self):
        return f"{self.username} places bid of {self.bid_price} on product {self.product_id}"
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
    product_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="auction_id")
    comment = models.TextField(max_length=200)

    def __str__(self):
        return f"On Product ID {self.product_id} User {self.username} comments {self.comment}"
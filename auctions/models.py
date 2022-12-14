from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=256)
    startbid = models.IntegerField()
    maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="maker")
    # winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", blank=True)
    category = models.CharField(max_length=64, blank=True)
    image = models.CharField(max_length=256, blank=True)
    activestatus = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, null = True, blank=True, related_name="watchlist")
    

class AuctionBids(models.Model):
    price = models.DecimalField(max_digits = 12, decimal_places = 2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bid_item")


class Comments(models.Model):
    comment_itself = models.CharField(max_length=256)
    comment_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_from")
    comment_on = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comment_on")

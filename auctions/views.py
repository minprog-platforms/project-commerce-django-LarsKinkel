from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, AuctionBids, Comments

# class Placebidform(forms.Form):
#     bid = forms.IntegerField(label="Place your bid")
#
# class Commentform(forms.Form):
#     comment = forms.CharField(widget=forms.Textarea(), label="Place your Comment")

def index(request):
    active_listings = AuctionListing.objects.filter(activestatus=True)

    return render(request, "auctions/index.html",{
        "active_listings": active_listings
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def createlisting(request):
    if request.method == "POST":
        title_ = request.POST["title"]
        description_ = request.POST["description"]
        startbid_ = int(request.POST["startbid"])
        category_ = request.POST["category"]
        image_ = request.POST["image"]
        maker_ = request.user

        newlist = AuctionListing(title = title_, description = description_, startbid = startbid_, image = image_, category = category_, maker = maker_)
        newlist.save()

        firstbid = AuctionBids(price = startbid_, bid_item = newlist, bidder = maker_)
        firstbid.save()

        return HttpResponseRedirect(reverse(index))
    return render(request, "auctions/createlisting.html")

@login_required
def placebid(request, listing_id):

    listing = AuctionListing.objects.get(pk=listing_id)
    currentbid = listing.startbid
    bid_item = listing

    if request.method == "POST":
        bid = request.POST["bid"]
        bidder = request.user
        highest_bid = AuctionBids.objects.filter(bid_item = bid_item).order_by('-price')[0].price

        if float(bid) > float(highest_bid):
            newbid = AuctionBids(price = bid, bid_item = bid_item, bidder = bidder)
            newbid.save()
            updated = True
            highest_bid = bid
        else:
            updated = False
    else:
        updated = ""

    comments = Comments.objects.filter(comment_on = listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "highest_bid": highest_bid,
        "updated": updated,
        "comments": comments
     })


# def comment(request, listing_id):
#     comment_on = AuctionListing.objects.get(pk=listing_id)
#
#
#
#     return render(request, "auctions/listing.html", {
#         "listing": comment_on,
#         "comments": Comments.objects.filter(comment_on = comment_on)
#      })


def listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    watchlistbutton = request.user in listing.watchlist.all()
    highest_bid = AuctionBids.objects.filter(bid_item = listing).order_by('-price')[0].price

    if request.method == "POST":
        comment_itself = request.POST["comment"]
        comment_from = request.user

        new_comment = Comments(
            comment_itself = comment_itself,
            comment_on = listing,
            comment_from = comment_from
        )
        new_comment.save()

    comments = Comments.objects.filter(comment_on = listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlistbutton": watchlistbutton,
        "highest_bid": highest_bid,
        "comments": comments
     })


@login_required
def add_watchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.watchlist.add(request.user)

    listingpage = AuctionListing.objects.get(id=listing_id)
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


@login_required
def remove_watchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.watchlist.remove(request.user)

    listingpage = AuctionListing.objects.get(id=listing_id)
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


@login_required
def watchlist(request):
    watching = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watching": watching
    })

@login_required
def close_listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.activestatus = False
    highest_bidder = AuctionBids.objects.filter(bid_item = listing).order_by('-price')[0].bidder
    listing.winner = highest_bidder
    listing.save()

    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

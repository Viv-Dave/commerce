from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment, Watchlist

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

def auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    latest_bid = Bid.objects.filter(product_id=listing).order_by('-bid_price').first()
    comments = Comment.objects.filter(product_id=listing)
    
    context = {
        "auction_item": listing.auction_item,
        "price": listing.price,
        "category": listing.category,
        "bidding_price": latest_bid.bid_price if latest_bid else listing.price,
        "bidder": latest_bid.username if latest_bid else "No bidders",
        "comments": comments,
        "auction_id": listing_id,
        "active_status": listing.active_status
    }
    
    return render(request, "auctions/auction.html", context)
# Sections where login is required
@login_required
def create_listing(request):
    if request.method == "POST":
        auction_item = request.POST["auction_item"]
        price = request.POST["price"]
        category = request.POST["category"]
        active_status = request.POST["active_status"]
        photo_url = request.FILES.get("photo_url", None)

        try:
            auction = Listing.objects.create(
                auction_item=auction_item,
                price=price,
                category=category,
                active_status=active_status,
                photo_url=photo_url,
                owner = request.user
            )
            auction.save()
            return redirect('index')
        
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    else:
        return render(request, "auctions/create.html")
@login_required
def add_watchlist(request, auction_id):
    listing = get_object_or_404(Listing, listing_id=auction_id)
    
    # Check if the item is already in the watchlist
    watchlist_item, created = Watchlist.objects.get_or_create(
        username=request.user,
        product_id=listing
    )

    if created:
        # Item was not in the watchlist, it has been added
        message = "Item added to your watchlist."
    else:
        # Item already exists in the watchlist
        message = "Item is already in your watchlist."

    return redirect('see_watchlist', username=request.user.username)

@login_required
def see_watchlist(request, username):
    if request.user.username != username:
        return redirect('index')  
    
    watchlist_items = Watchlist.objects.filter(username=request.user)

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist_items
    })
@login_required
def create_auction(request, username):
    if request.user.username != username:
        return redirect('index')
    
    return render(request, "auctions/create.html")

@login_required
def your_listings(request, username):
    if request.user.username != username:
        return redirect('index')

    user_listings = Listing.objects.filter(owner=request.user)
    return render(request, "auctions/listing.html", {
        "listings": user_listings
    })

@login_required
def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id, owner=request.user)

    if request.method == "POST":
        listing.active_status = False
        listing.save()
        return redirect('your_listings', username=request.user.username)
    
    return render(request, "auctions/close_listing.html", {
        "listing": listing
    })

@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    current_highest_bid = Bid.objects.filter(product_id=listing).order_by('-bid_price').first()
    
    if request.method == "POST":
        bid_amount = int(request.POST["bid_amount"])
        # Check if the bid is higher than both the starting price and current highest bid
        if current_highest_bid:
            min_bid = current_highest_bid.bid_price
        else:
            min_bid = listing.price
            
        if bid_amount > min_bid:
            # Create the new bid
            Bid.objects.create(
                username=request.user,
                product_id=listing,
                bid_price=bid_amount
            )
            return redirect('auction', listing_id=listing_id)
        else:
            return HttpResponse("Bid must be higher than the current price!")
    else:
        return redirect('auction', listing_id=listing_id)

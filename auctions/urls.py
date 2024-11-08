from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:auction_id>", views.auction, name="auction"),
    path('add_watchlist/<int:auction_id>/', views.add_watchlist, name='add_watchlist'),
    path('watchlist/<str:username>/', views.see_watchlist, name='see_watchlist'),
    path("create/<str:username>/", views.create_auction, name="create_auction"),
    path("create", views.create_listing, name="creating_listing")
]

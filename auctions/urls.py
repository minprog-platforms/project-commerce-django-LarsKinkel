from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("<int:listing_id>", views.listing, name="listing"),
    # path("<int:listing_id>", views.change_watchlist, name="change_watchlist"),
    path("<int:listing_id>/add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("<int:listing_id>/remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/placebid", views.placebid, name="placebid"),
    path("<int:listing_id>/closelisting", views.close_listing, name="close_listing")
]

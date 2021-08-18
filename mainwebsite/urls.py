from mainwebsite import views
from django.urls import path

urlpatterns = [
    path("",views.homePage),
    path("artists/",views.artistsListPage),
    path("artist/<int:id>/",views.artistPage),
    path("artwork/<int:id>",views.productDetailsPage),
    path("about/",views.aboutPage),
    path("cart/",views.cartPage),
    path("checkout/",views.checkoutPage),
    path("success-order/<str:order_id>/",views.successPage),
    path("orders/",views.orders_search),
    path("orders/<str:order_id>/", views.orders_details),

]
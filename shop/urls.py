from django.urls import path
from .views import index, addtocart, cart_view, remove_from_cart,search_product,checkout,order_history

urlpatterns = [
    path('', index, name='index'),  # Liste des produits
    path('<int:id>/', index, name='product_detail'),  # Détail d'un produit
    path('cart/', cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', addtocart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/<str:size>/', remove_from_cart, name='remove_from_cart'),
    path('search/', search_product, name='search_product'),
    path('checkout/', checkout, name='checkout'),  #  Nouvelle route pour la commande
    path('order-history/', order_history, name='order_history'),  #  Ajout de l'historique
]
